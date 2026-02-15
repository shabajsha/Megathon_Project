# MERN Stack Event Management System - Quick Start Guide

## 🎯 What Has Been Implemented

This project is a comprehensive event management system built with the MERN stack (MongoDB, Express.js, React, Node.js).

### ✅ Backend (Fully Functional)

**Models:**
- ✅ Participant (with IIIT email validation)
- ✅ Organizer (provisioned by admin)
- ✅ Admin (first user in system)
- ✅ Event (Normal & Merchandise types)

**Authentication & Security:**
- ✅ JWT-based authentication
- ✅ bcrypt password hashing
- ✅ Role-based access control middleware
- ✅ IIIT email domain validation (@iiit.ac.in)

**API Endpoints:**
- ✅ Authentication routes (register, login for all roles)
- ✅ Participant routes (profile, preferences, follow/unfollow)
- ✅ Organizer routes (profile, event management)
- ✅ Admin routes (create/remove organizers)
- ✅ Event routes (CRUD, registration, filters, trending)

**Features:**
- ✅ Custom registration forms for events
- ✅ QR code generation for tickets
- ✅ Email notifications (configured but requires SMTP setup)
- ✅ Event search and filtering
- ✅ Trending events (last 24 hours)
- ✅ Stock management for merchandise
- ✅ Attendance tracking

### ✅ Frontend (Core Features)

**Authentication:**
- ✅ Login page with role selection (Participant/Organizer/Admin)
- ✅ Registration page with IIIT email validation
- ✅ Authentication context with localStorage persistence
- ✅ Private routes with role-based access

**UI Components:**
- ✅ Responsive navbar
- ✅ Participant dashboard (basic)
- ✅ Form components with validation
- ✅ Error handling and loading states

**Services:**
- ✅ Axios API service with interceptors
- ✅ Token management
- ✅ Auto-redirect on auth failure

## 🚀 How to Run

### Option 1: Using the start script (Linux/Mac)
```bash
./start-dev.sh
```

### Option 2: Manual setup

**Terminal 1 - Backend:**
```bash
cd backend
npm install
cp .env.example .env
# Edit .env if needed (MongoDB URI, JWT secret, etc.)
npm run dev
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Initialize Admin Account

Make a POST request to initialize the admin:
```bash
curl -X POST http://localhost:5000/api/admin/init
```

Default admin credentials (from backend/.env):
- Email: admin@eventmanagement.com
- Password: Admin@12345

## 📝 Usage Flow

### As Participant:
1. Register at `/register`
   - IIIT students: Use @iiit.ac.in email
   - Others: Use any email
2. Login at `/login` → Select "Participant"
3. Access dashboard at `/participant/dashboard`
4. Browse events, register, manage profile

### As Organizer:
1. Admin creates your account
2. Login at `/login` → Select "Organizer"
3. Access dashboard at `/organizer/dashboard`
4. Create events, manage registrations

### As Admin:
1. Login at `/login` → Select "Admin"
   - Email: admin@eventmanagement.com
   - Password: Admin@12345
2. Access dashboard at `/admin/dashboard`
3. Create/manage organizer accounts

## 🔧 Configuration

### Backend Environment Variables (.env)
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/event-management
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRE=7d
ADMIN_EMAIL=admin@eventmanagement.com
ADMIN_PASSWORD=Admin@12345
```

### Frontend Environment Variables (.env)
```
VITE_API_URL=http://localhost:5000/api
```

## 📚 API Documentation

### Authentication
- `POST /api/auth/register/participant` - Register new participant
- `POST /api/auth/login/participant` - Participant login
- `POST /api/auth/login/organizer` - Organizer login
- `POST /api/auth/login/admin` - Admin login

### Events
- `GET /api/events` - Get all events (with filters)
- `GET /api/events/trending` - Get trending events
- `GET /api/events/:id` - Get event details
- `POST /api/events` - Create event (Organizer)
- `PUT /api/events/:id` - Update event (Organizer)
- `POST /api/events/:id/register` - Register for event (Participant)

### Participants
- `GET /api/participants/profile` - Get profile
- `PUT /api/participants/profile` - Update profile
- `POST /api/participants/preferences` - Set preferences
- `POST /api/participants/follow/:organizerId` - Follow/unfollow
- `GET /api/participants/my-events` - Get registered events

### Admin
- `POST /api/admin/init` - Initialize admin
- `POST /api/admin/organizers` - Create organizer
- `GET /api/admin/organizers` - List all organizers
- `DELETE /api/admin/organizers/:id` - Remove organizer

## 🎨 Tech Stack

**Backend:**
- Node.js + Express.js
- MongoDB + Mongoose
- JWT + bcrypt
- Nodemailer
- QRCode

**Frontend:**
- React 19
- Vite
- React Router v7
- Axios
- Context API

## 📋 What's Next (To Complete Assignment)

### Frontend Pages to Build:
- [ ] Event browsing page with search/filters
- [ ] Event details page
- [ ] Event registration page
- [ ] Clubs/Organizers listing page
- [ ] Full participant profile page
- [ ] Organizer dashboard
- [ ] Event creation/editing interface
- [ ] Admin dashboard
- [ ] Organizer management interface

### Advanced Features (Part 2):
- [ ] Choose 2 from Tier A (8 marks each)
- [ ] Choose 2 from Tier B (6 marks each)
- [ ] Choose 1 from Tier C (2 marks)

### Deployment:
- [ ] Deploy backend to Render/Railway/Heroku
- [ ] Deploy frontend to Vercel/Netlify
- [ ] Create deployment.txt with URLs

## 🐛 Troubleshooting

**MongoDB Connection Error:**
- Make sure MongoDB is running: `mongod` or use MongoDB Atlas
- Update MONGODB_URI in backend/.env

**Port Already in Use:**
- Backend: Change PORT in backend/.env
- Frontend: Change port in vite.config.js

**CORS Issues:**
- Backend has CORS enabled for all origins in development
- Update CORS settings for production

## 📄 License

This project is part of an academic assignment for Megathon.

## ✅ Assignment Checklist

Based on assignment1.md requirements:

**Part 1: Core System (70 marks)**
- ✅ Authentication & Security (8 marks) - Implemented
- ✅ User Onboarding & Preferences (3 marks) - Implemented
- ✅ User Data Models (2 marks) - Implemented
- ✅ Event Types (2 marks) - Implemented
- ✅ Event Attributes (2 marks) - Implemented
- 🔄 Participant Features (22 marks) - Partially implemented (API done, UI in progress)
- 🔄 Organizer Features (18 marks) - API done, UI pending
- 🔄 Admin Features (6 marks) - API done, UI pending
- ⏳ Deployment (5 marks) - Pending

**Part 2: Advanced Features (30 marks)**
- ⏳ Tier A - Choose 2 (16 marks) - Pending
- ⏳ Tier B - Choose 2 (12 marks) - Pending
- ⏳ Tier C - Choose 1 (2 marks) - Pending

**Status:** Backend 100% complete, Frontend 30% complete
