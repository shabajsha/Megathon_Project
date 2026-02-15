import api from './api';

// Auth Services
export const authService = {
  registerParticipant: (data) => api.post('/auth/register/participant', data),
  loginParticipant: (data) => api.post('/auth/login/participant', data),
  loginOrganizer: (data) => api.post('/auth/login/organizer', data),
  loginAdmin: (data) => api.post('/auth/login/admin', data),
};

// Participant Services
export const participantService = {
  getProfile: () => api.get('/participants/profile'),
  updateProfile: (data) => api.put('/participants/profile', data),
  setPreferences: (data) => api.post('/participants/preferences', data),
  followOrganizer: (organizerId) => api.post(`/participants/follow/${organizerId}`),
  getMyEvents: () => api.get('/participants/my-events'),
};

// Event Services
export const eventService = {
  getAllEvents: (params) => api.get('/events', { params }),
  getTrendingEvents: () => api.get('/events/trending'),
  getEventById: (eventId) => api.get(`/events/${eventId}`),
  createEvent: (data) => api.post('/events', data),
  updateEvent: (eventId, data) => api.put(`/events/${eventId}`, data),
  publishEvent: (eventId) => api.put(`/events/${eventId}/publish`),
  registerForEvent: (eventId, data) => api.post(`/events/${eventId}/register`, data),
  getEventRegistrations: (eventId) => api.get(`/events/${eventId}/registrations`),
};

// Organizer Services
export const organizerService = {
  getProfile: () => api.get('/organizers/profile'),
  updateProfile: (data) => api.put('/organizers/profile', data),
  getAllOrganizers: () => api.get('/organizers/list'),
  getOrganizerById: (organizerId) => api.get(`/organizers/${organizerId}`),
};

// Admin Services
export const adminService = {
  initAdmin: () => api.post('/admin/init'),
  createOrganizer: (data) => api.post('/admin/organizers', data),
  getAllOrganizers: () => api.get('/admin/organizers'),
  removeOrganizer: (organizerId, permanent) => 
    api.delete(`/admin/organizers/${organizerId}`, { params: { permanent } }),
  activateOrganizer: (organizerId) => 
    api.put(`/admin/organizers/${organizerId}/activate`),
};
