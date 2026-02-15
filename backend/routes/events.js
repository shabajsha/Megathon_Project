const express = require('express');
const router = express.Router();
const { authenticate, isOrganizer, isParticipant } = require('../middleware/auth');
const Event = require('../models/Event');
const Participant = require('../models/Participant');
const { generateQRCode, generateTicketId } = require('../utils/qrcode');
const { sendTicketEmail } = require('../utils/email');

// Create new event (Organizer only)
router.post('/', authenticate, isOrganizer, async (req, res) => {
  try {
    const eventData = {
      ...req.body,
      organizer: req.userId,
      status: 'Draft'
    };

    const event = new Event(eventData);
    await event.save();

    res.status(201).json({
      message: 'Event created successfully',
      event
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Get all events (with filters)
router.get('/', async (req, res) => {
  try {
    const { search, type, eligibility, status, organizerId, followed, participantId } = req.query;
    
    let query = { status: { $in: ['Published', 'Ongoing'] } };

    if (search) {
      query.$text = { $search: search };
    }

    if (type) {
      query.eventType = type;
    }

    if (eligibility) {
      query.eligibility = eligibility;
    }

    if (status) {
      query.status = status;
    }

    if (organizerId) {
      query.organizer = organizerId;
    }

    // Filter by followed clubs
    if (followed === 'true' && participantId) {
      const participant = await Participant.findById(participantId);
      query.organizer = { $in: participant.followedClubs };
    }

    const events = await Event.find(query)
      .populate('organizer', 'organizerName category')
      .sort({ createdAt: -1 });

    res.json(events);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Get trending events (top 5 in last 24 hours)
router.get('/trending', async (req, res) => {
  try {
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000);
    
    const events = await Event.find({
      status: 'Published',
      createdAt: { $gte: yesterday }
    })
    .populate('organizer', 'organizerName category')
    .sort({ totalRegistrations: -1 })
    .limit(5);

    res.json(events);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Get event by ID
router.get('/:eventId', async (req, res) => {
  try {
    const event = await Event.findById(req.params.eventId)
      .populate('organizer', 'organizerName category description contactEmail');

    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }

    res.json(event);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Update event (Organizer only)
router.put('/:eventId', authenticate, isOrganizer, async (req, res) => {
  try {
    const event = await Event.findById(req.params.eventId);

    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }

    // Check if organizer owns the event
    if (event.organizer.toString() !== req.userId) {
      return res.status(403).json({ message: 'Not authorized to edit this event' });
    }

    // Editing rules based on status
    if (event.status === 'Draft') {
      // Free edits for draft
      Object.assign(event, req.body);
    } else if (event.status === 'Published') {
      // Limited edits for published
      const allowedFields = ['eventDescription', 'registrationDeadline', 'registrationLimit'];
      allowedFields.forEach(field => {
        if (req.body[field] !== undefined) {
          event[field] = req.body[field];
        }
      });
    } else if (event.status === 'Ongoing' || event.status === 'Completed') {
      // Only status change allowed
      if (req.body.status) {
        event.status = req.body.status;
      } else {
        return res.status(400).json({ message: 'Only status can be changed for ongoing/completed events' });
      }
    }

    await event.save();

    res.json({
      message: 'Event updated successfully',
      event
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Publish event
router.put('/:eventId/publish', authenticate, isOrganizer, async (req, res) => {
  try {
    const event = await Event.findById(req.params.eventId);

    if (!event || event.organizer.toString() !== req.userId) {
      return res.status(403).json({ message: 'Not authorized' });
    }

    event.status = 'Published';
    await event.save();

    res.json({ message: 'Event published successfully', event });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Register for event (Participant only)
router.post('/:eventId/register', authenticate, isParticipant, async (req, res) => {
  try {
    const event = await Event.findById(req.params.eventId).populate('organizer');
    const participant = await Participant.findById(req.userId);

    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }

    // Validate registration
    if (event.status !== 'Published') {
      return res.status(400).json({ message: 'Event is not open for registration' });
    }

    if (new Date() > event.registrationDeadline) {
      return res.status(400).json({ message: 'Registration deadline has passed' });
    }

    if (event.totalRegistrations >= event.registrationLimit) {
      return res.status(400).json({ message: 'Registration limit reached' });
    }

    // Check eligibility
    if (event.eligibility === 'IIIT Only' && participant.participantType !== 'IIIT') {
      return res.status(403).json({ message: 'This event is only for IIIT students' });
    }

    if (event.eligibility === 'Non-IIIT Only' && participant.participantType === 'IIIT') {
      return res.status(403).json({ message: 'This event is only for Non-IIIT participants' });
    }

    // Check if already registered
    const alreadyRegistered = event.registrations.some(
      reg => reg.participant.toString() === req.userId
    );

    if (alreadyRegistered) {
      return res.status(400).json({ message: 'Already registered for this event' });
    }

    // Generate ticket
    const ticketId = generateTicketId();
    const qrCode = await generateQRCode({
      ticketId,
      eventId: event._id,
      participantId: participant._id,
      eventName: event.eventName
    });

    // Add registration
    event.registrations.push({
      participant: req.userId,
      formData: req.body.formData || {},
      ticketId,
      paymentStatus: 'Completed'
    });

    event.totalRegistrations += 1;
    event.totalRevenue += event.registrationFee;

    // Lock form after first registration
    if (event.totalRegistrations === 1) {
      event.isFormLocked = true;
    }

    await event.save();

    // Add event to participant's registered events
    participant.registeredEvents.push(event._id);
    await participant.save();

    // Send ticket email
    await sendTicketEmail(participant.email, `Registration Confirmation - ${event.eventName}`, {
      participantName: `${participant.firstName} ${participant.lastName}`,
      eventName: event.eventName,
      ticketId,
      eventDate: event.eventStartDate.toDateString()
    });

    res.status(201).json({
      message: 'Registration successful',
      ticketId,
      qrCode
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Get event registrations (Organizer only)
router.get('/:eventId/registrations', authenticate, isOrganizer, async (req, res) => {
  try {
    const event = await Event.findById(req.params.eventId)
      .populate('registrations.participant', 'firstName lastName email contactNumber');

    if (!event || event.organizer.toString() !== req.userId) {
      return res.status(403).json({ message: 'Not authorized' });
    }

    res.json(event.registrations);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

module.exports = router;
