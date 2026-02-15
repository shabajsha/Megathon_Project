# Event Management System - MERN Stack

A comprehensive event management platform built with MongoDB, Express.js, React, and Node.js for managing events, clubs, and participants.

## 🎯 Features

### Core Features (70 Marks)
- ✅ **Authentication & Security** (8 marks)
  - JWT-based authentication
  - bcrypt password hashing
  - Role-based access control
  - IIIT email validation for students

- ✅ **User Roles**
  - Participants (IIIT & Non-IIIT)
  - Organizers (Clubs, Councils, Fest Teams)
  - Admin (System administrator)

- ✅ **Event Management**
  - Normal events with custom registration forms
  - Merchandise events with stock management
  - Event filtering, search, and trending
  - QR code ticketing system

- ✅ **Participant Features**
  - Browse and register for events
  - Follow clubs/organizers
  - Participation history
  - Profile management

- ✅ **Organizer Features**
  - Create and manage events
  - Analytics dashboard
  - Participant management
  - Discord webhook integration

- ✅ **Admin Features**
  - Create/remove organizer accounts
  - Club/organizer management

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- MongoDB
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Megathon_Project
   ```

2. **Backend Setup**
   ```bash
   cd backend
   npm install
   cp .env.example .env
   # Edit .env with your configuration
   npm run dev
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Edit .env with your API URL
   npm run dev
   ```

4. **Initialize Admin Account**
   ```bash
   # Make a POST request to create admin
   curl -X POST http://localhost:5000/api/admin/init
   ```

## 📁 Project Structure

```
Megathon_Project/
├── backend/
│   ├── config/
│   ├── controllers/
│   ├── middleware/
│   │   └── auth.js
│   ├── models/
│   │   ├── Admin.js
│   │   ├── Event.js
│   │   ├── Organizer.js
│   │   └── Participant.js
│   ├── routes/
│   │   ├── admin.js
│   │   ├── auth.js
│   │   ├── events.js
│   │   ├── organizers.js
│   │   └── participants.js
│   ├── utils/
│   │   ├── email.js
│   │   ├── jwt.js
│   │   └── qrcode.js
│   ├── .env.example
│   ├── package.json
│   └── server.js
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── PrivateRoute.jsx
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── ParticipantDashboard.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── index.js
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔑 Environment Variables

### Backend (.env)
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/event-management
JWT_SECRET=your-secret-key
JWT_EXPIRE=7d
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-password
ADMIN_EMAIL=admin@eventmanagement.com
ADMIN_PASSWORD=Admin@12345
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000/api
```

## 🧪 API Endpoints

### Authentication
- `POST /api/auth/register/participant` - Register participant
- `POST /api/auth/login/participant` - Participant login
- `POST /api/auth/login/organizer` - Organizer login
- `POST /api/auth/login/admin` - Admin login

### Events
- `GET /api/events` - Get all events (with filters)
- `GET /api/events/trending` - Get trending events
- `GET /api/events/:eventId` - Get event details
- `POST /api/events` - Create event (Organizer)
- `PUT /api/events/:eventId` - Update event (Organizer)
- `POST /api/events/:eventId/register` - Register for event (Participant)

### Participants
- `GET /api/participants/profile` - Get profile
- `PUT /api/participants/profile` - Update profile
- `POST /api/participants/preferences` - Set preferences
- `POST /api/participants/follow/:organizerId` - Follow/unfollow organizer
- `GET /api/participants/my-events` - Get registered events

### Organizers
- `GET /api/organizers/list` - Get all organizers
- `GET /api/organizers/:organizerId` - Get organizer details
- `GET /api/organizers/profile` - Get profile (Auth required)
- `PUT /api/organizers/profile` - Update profile (Auth required)

### Admin
- `POST /api/admin/init` - Initialize admin account
- `POST /api/admin/organizers` - Create organizer account
- `GET /api/admin/organizers` - Get all organizers
- `DELETE /api/admin/organizers/:organizerId` - Remove organizer

## 🎨 Tech Stack

- **Frontend**: React, Vite, React Router, Axios
- **Backend**: Node.js, Express.js
- **Database**: MongoDB, Mongoose
- **Authentication**: JWT, bcrypt
- **Email**: Nodemailer
- **QR Codes**: qrcode library

## 📝 License

This project is part of an academic assignment.

## 👥 Authors

- Developed as part of Megathon Project assignment
