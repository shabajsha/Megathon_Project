const nodemailer = require('nodemailer');

// Create email transporter
const createTransporter = () => {
  return nodemailer.createTransporter({
    host: process.env.EMAIL_HOST,
    port: process.env.EMAIL_PORT,
    secure: false,
    auth: {
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS,
    },
  });
};

// Send email with ticket
exports.sendTicketEmail = async (to, subject, ticketData) => {
  try {
    const transporter = createTransporter();
    
    const mailOptions = {
      from: process.env.EMAIL_USER,
      to: to,
      subject: subject,
      html: `
        <h2>Event Registration Confirmation</h2>
        <p>Dear ${ticketData.participantName},</p>
        <p>You have successfully registered for <strong>${ticketData.eventName}</strong>.</p>
        <p><strong>Ticket ID:</strong> ${ticketData.ticketId}</p>
        <p><strong>Event Date:</strong> ${ticketData.eventDate}</p>
        <p>Please keep this email for your records.</p>
        <p>QR Code and full ticket details are available in your dashboard.</p>
        <br>
        <p>Best regards,<br>Event Management Team</p>
      `,
    };

    await transporter.sendMail(mailOptions);
    return true;
  } catch (error) {
    console.error('Email sending failed:', error);
    return false;
  }
};

// Send organizer credentials
exports.sendOrganizerCredentials = async (to, credentials) => {
  try {
    const transporter = createTransporter();
    
    const mailOptions = {
      from: process.env.EMAIL_USER,
      to: to,
      subject: 'Your Organizer Account Credentials',
      html: `
        <h2>Welcome to Event Management System</h2>
        <p>Your organizer account has been created.</p>
        <p><strong>Login Email:</strong> ${credentials.email}</p>
        <p><strong>Password:</strong> ${credentials.password}</p>
        <p>Please change your password after first login.</p>
        <br>
        <p>Best regards,<br>Admin Team</p>
      `,
    };

    await transporter.sendMail(mailOptions);
    return true;
  } catch (error) {
    console.error('Email sending failed:', error);
    return false;
  }
};
