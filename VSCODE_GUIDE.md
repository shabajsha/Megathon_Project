# 🎯 Running the MERN Event Management System in VS Code

This guide will help you set up and run the Event Management System in Visual Studio Code with full debugging capabilities.

## 📋 Prerequisites

Before you begin, ensure you have:
- ✅ [Visual Studio Code](https://code.visualstudio.com/) installed
- ✅ [Node.js](https://nodejs.org/) (v14 or higher)
- ✅ [MongoDB](https://www.mongodb.com/try/download/community) installed and running, OR
- ✅ [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account (cloud database)

## 🚀 Quick Start in VS Code

### Step 1: Open Project in VS Code

```bash
# Navigate to project directory
cd /path/to/Megathon_Project

# Open in VS Code
code .
```

Or simply:
- Open VS Code
- File → Open Folder
- Select the `Megathon_Project` folder

### Step 2: Install Recommended Extensions

When you first open the project, VS Code will prompt you to install recommended extensions. Click **"Install All"**.

**Essential Extensions:**
- ESLint - JavaScript linting
- Prettier - Code formatter
- ES7+ React/Redux/React-Native snippets
- MongoDB for VS Code
- npm Intellisense
- Path Intellisense

### Step 3: Install Dependencies

**Option A: Using VS Code Tasks (Recommended)**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Tasks: Run Task"
3. Select "Install All Dependencies"

**Option B: Using Terminal**
```bash
# In VS Code terminal (Ctrl+` or View → Terminal)
cd backend
npm install
cd ../frontend
npm install
```

### Step 4: Configure Environment Variables

1. **Backend Configuration:**
   ```bash
   cd backend
   cp .env.example .env
   ```
   
   Edit `backend/.env` and update:
   ```env
   MONGODB_URI=mongodb://localhost:27017/event-management
   JWT_SECRET=your-secret-key-here
   ```

2. **Frontend Configuration:**
   ```bash
   cd frontend
   cp .env.example .env
   ```
   
   The default settings should work:
   ```env
   VITE_API_URL=http://localhost:5000/api
   ```

### Step 5: Run the Application

**Option A: Run Full Stack (Recommended)**

1. Press `Ctrl+Shift+D` (or `Cmd+Shift+D` on Mac) to open Run and Debug
2. Select "**Run Full Stack**" from the dropdown
3. Press `F5` or click the green play button

This will start both backend and frontend servers!

**Option B: Run Backend and Frontend Separately**

Using Tasks:
1. Press `Ctrl+Shift+P` → "Tasks: Run Task"
2. Select "backend: dev" (starts backend on port 5000)
3. Repeat and select "frontend: dev" (starts frontend on port 5173)

**Option C: Using Terminal**
```bash
# Terminal 1 - Backend
cd backend
npm run dev

# Terminal 2 - Frontend (new terminal with Ctrl+Shift+`)
cd frontend
npm run dev
```

### Step 6: Initialize Admin Account

After the backend is running:

**Using VS Code Task:**
1. Press `Ctrl+Shift+P` → "Tasks: Run Task"
2. Select "Initialize Admin"

**Or use terminal:**
```bash
curl -X POST http://localhost:5000/api/admin/init
```

### Step 7: Access the Application

🌐 **Frontend:** http://localhost:5173
🔧 **Backend API:** http://localhost:5000/api

**Default Admin Credentials:**
- Email: `admin@eventmanagement.com`
- Password: `Admin@12345`

---

## 🐛 Debugging in VS Code

### Debug Backend

1. Set breakpoints in your backend code by clicking left of line numbers
2. Press `Ctrl+Shift+D` to open Run and Debug
3. Select "**Backend: Debug**" from dropdown
4. Press `F5` to start debugging
5. The debugger will pause at your breakpoints

### Debug Frontend

1. Set breakpoints in your React code
2. Select "**Frontend: Debug**" from the debug dropdown
3. Press `F5` to start
4. Browser will open with debugging enabled

### Debug Full Stack

1. Select "**Full Stack**" from the debug dropdown
2. Press `F5`
3. Both backend and frontend will start with debugging enabled
4. Set breakpoints in either backend or frontend code

---

## 📦 VS Code Tasks Reference

Access tasks via: `Ctrl+Shift+P` → "Tasks: Run Task"

### Development Tasks
- **Install All Dependencies** - Install npm packages for both backend and frontend
- **backend: dev** - Start backend development server with hot reload
- **frontend: dev** - Start frontend development server with hot reload
- **Run Full Stack** - Start both backend and frontend

### Build Tasks
- **frontend: build** - Build frontend for production
- **frontend: preview** - Preview production build locally

### Utility Tasks
- **Initialize Admin** - Create admin account in database
- **backend: start** - Start backend in production mode

---

## 🎨 Code Formatting & Linting

The project is configured with ESLint and Prettier:

### Auto-format on Save
Files will automatically format when you save (enabled by default in `.vscode/settings.json`)

### Manual Formatting
- Format current file: `Shift+Alt+F` (or `Shift+Option+F` on Mac)
- Format on paste: Enabled by default

### Fix ESLint Issues
1. Open Command Palette: `Ctrl+Shift+P`
2. Type "ESLint: Fix all auto-fixable Problems"
3. Press Enter

---

## 🔍 Useful VS Code Shortcuts

### Navigation
- `Ctrl+P` - Quick file open
- `Ctrl+Shift+F` - Search across all files
- `Ctrl+G` - Go to line
- `Ctrl+B` - Toggle sidebar
- `Ctrl+`` - Toggle terminal

### Editing
- `Ctrl+D` - Select next occurrence
- `Alt+Up/Down` - Move line up/down
- `Shift+Alt+Up/Down` - Duplicate line
- `Ctrl+/` - Toggle line comment
- `Shift+Alt+F` - Format document

### Debugging
- `F5` - Start/Continue debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into
- `Shift+F11` - Step out
- `Shift+F5` - Stop debugging

---

## 📂 Project Structure in VS Code

```
Megathon_Project/
├── .vscode/                    # VS Code configuration
│   ├── launch.json            # Debug configurations
│   ├── tasks.json             # Task definitions
│   ├── settings.json          # Workspace settings
│   └── extensions.json        # Recommended extensions
├── backend/                    # Express.js backend
│   ├── models/                # Database models
│   ├── routes/                # API routes
│   ├── middleware/            # Auth middleware
│   ├── utils/                 # Utilities (JWT, email, QR)
│   └── server.js              # Entry point
├── frontend/                   # React frontend
│   └── src/
│       ├── components/        # Reusable components
│       ├── pages/             # Page components
│       ├── contexts/          # React contexts
│       ├── services/          # API services
│       └── App.jsx            # Main app component
└── Documentation/
    ├── VSCODE_GUIDE.md        # This file
    ├── QUICKSTART.md          # Quick start guide
    └── README_MERN.md         # Project documentation
```

---

## 🛠️ Troubleshooting

### Port Already in Use

If you get "port already in use" error:

**Backend (Port 5000):**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows (find PID, then kill)
```

**Frontend (Port 5173):**
```bash
# Find and kill process on port 5173
lsof -ti:5173 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5173   # Windows
```

### MongoDB Connection Error

If backend can't connect to MongoDB:

1. **Check MongoDB is running:**
   ```bash
   # Mac (Homebrew)
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   
   # Windows
   net start MongoDB
   ```

2. **Or use MongoDB Atlas:**
   - Sign up at https://www.mongodb.com/cloud/atlas
   - Create a free cluster
   - Get connection string
   - Update `backend/.env`:
     ```
     MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/event-management
     ```

### ESLint Not Working

1. Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"
2. Check ESLint output: View → Output → Select "ESLint" from dropdown
3. Reinstall dependencies: `npm install` in backend and frontend folders

### Debugger Not Attaching

1. Make sure server is running
2. Check port numbers in `.vscode/launch.json` match your configuration
3. Try restarting VS Code

---

## 📝 Development Workflow

### Typical Development Session

1. **Open VS Code** to project folder
2. **Start servers** using "Run Full Stack" debug configuration
3. **Make changes** to code (auto-saves and hot-reloads)
4. **Set breakpoints** where needed
5. **Test in browser** at http://localhost:5173
6. **Check API** responses in VS Code terminal
7. **Commit changes** using VS Code's Source Control panel (`Ctrl+Shift+G`)

### Making Changes

#### Backend Changes
1. Edit files in `backend/` folder
2. Server auto-restarts (nodemon)
3. Check terminal for errors
4. Test API endpoints

#### Frontend Changes
1. Edit files in `frontend/src/` folder
2. Browser auto-refreshes (Vite HMR)
3. Check browser console for errors
4. See changes instantly

---

## 🎓 Learning Resources

### VS Code
- [VS Code Keyboard Shortcuts PDF](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
- [VS Code Tips and Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)

### Debugging
- [Debugging in VS Code](https://code.visualstudio.com/docs/editor/debugging)
- [Node.js Debugging](https://code.visualstudio.com/docs/nodejs/nodejs-debugging)

### Project Specific
- See `QUICKSTART.md` for API documentation
- See `README_MERN.md` for project overview
- See `assignment1.md` for requirements

---

## ✅ Quick Checklist

Before starting development, ensure:
- [ ] VS Code installed
- [ ] Recommended extensions installed
- [ ] Node.js and npm installed
- [ ] MongoDB running (local or Atlas)
- [ ] Dependencies installed (`npm install` in both folders)
- [ ] Environment variables configured (`.env` files)
- [ ] Admin account initialized
- [ ] Both servers running successfully

---

## 🆘 Getting Help

If you encounter issues:

1. **Check terminal output** for error messages
2. **Read error messages** carefully - they usually point to the problem
3. **Check MongoDB connection** - most common issue
4. **Verify environment variables** are set correctly
5. **Check ports** - make sure 5000 and 5173 are available
6. **Restart VS Code** - sometimes helps with extension issues
7. **Clear node_modules** and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

---

## 🎉 You're Ready!

Your VS Code is now fully configured for MERN stack development with:
- ✅ One-click debugging for frontend and backend
- ✅ Integrated task running
- ✅ Auto-formatting and linting
- ✅ Hot module replacement (HMR)
- ✅ Intelligent code completion
- ✅ Git integration

**Happy Coding! 🚀**
