# 🎉 VS Code Setup Complete!

Your MERN Event Management System is now fully configured for Visual Studio Code!

## 🚀 Quick Start (3 Easy Steps)

### Step 1: Open in VS Code
```bash
cd /path/to/Megathon_Project
code .
```

### Step 2: Install Recommended Extensions
When VS Code opens, you'll see a popup: **"This workspace has extension recommendations"**
- Click **"Install All"**

Or manually:
1. Press `Ctrl+Shift+X` (Extensions panel)
2. Search for "workspace recommendations"
3. Install the recommended extensions

### Step 3: Run the Application
**Method A: Using Debug (Recommended)**
1. Press `F5` (or click the Debug icon on left sidebar)
2. Select **"Run Full Stack"** from the dropdown menu
3. Press `F5` again or click the green ▶ button

**Method B: Using Tasks**
1. Press `Ctrl+Shift+P` (Command Palette)
2. Type "Tasks: Run Task"
3. Select **"Run Full Stack"**

**That's it!** Both backend and frontend will start automatically! 🎉

---

## 📁 What's Been Configured

### ✅ Debug Configurations (`.vscode/launch.json`)
Ready-to-use debugging setups:
- **Run Full Stack** - Start both backend and frontend with debugging
- **Backend: Debug** - Debug Express.js backend
- **Frontend: Debug** - Debug React app in Chrome
- **Backend: Attach** - Attach to running Node.js process

### ✅ Tasks (`.vscode/tasks.json`)
One-click operations:
- **Install All Dependencies** - Run npm install for both projects
- **Run Full Stack** - Start both servers
- **backend: dev** - Start backend with hot reload
- **frontend: dev** - Start frontend with Vite
- **frontend: build** - Build for production
- **Initialize Admin** - Create admin account

### ✅ Workspace Settings (`.vscode/settings.json`)
Automatic code quality:
- ✨ Auto-format on save (Prettier)
- 🔧 Auto-fix ESLint errors
- 📝 Smart import updates
- 🎨 Emmet for JSX
- 🗂️ Optimized file exclusions

### ✅ Recommended Extensions (`.vscode/extensions.json`)
Best tools for MERN development:
- **ESLint** - JavaScript linting
- **Prettier** - Code formatting
- **ES7+ React Snippets** - React code shortcuts
- **MongoDB** - Database management
- **npm Intellisense** - Package autocomplete
- **Path Intellisense** - File path autocomplete
- And more...

---

## 🎯 How to Use

### Running the Project

#### Option 1: Full Stack Debug (Best for Development)
```
Press F5 → Select "Run Full Stack" → Press F5 again
```
- Backend starts on http://localhost:5000
- Frontend starts on http://localhost:5173
- Both are debuggable with breakpoints!

#### Option 2: Individual Servers
**Backend Only:**
- Press F5 → Select "Backend: Debug"

**Frontend Only:**
- Press F5 → Select "Frontend: Debug"

#### Option 3: Tasks (No Debugging)
```
Ctrl+Shift+P → "Tasks: Run Task" → Select task
```

### Debugging Your Code

1. **Set Breakpoints**
   - Click to the left of line numbers in your code
   - Red dot appears = breakpoint set

2. **Start Debugging**
   - Press `F5`
   - Select debug configuration
   - Code will pause at breakpoints

3. **Debug Controls**
   - `F5` - Continue
   - `F10` - Step Over
   - `F11` - Step Into
   - `Shift+F11` - Step Out
   - `Shift+F5` - Stop

4. **Inspect Variables**
   - Hover over variables to see values
   - Use Debug panel to watch variables
   - View call stack and scope

### Common Tasks

#### Install Dependencies
```
Ctrl+Shift+P → "Tasks: Run Task" → "Install All Dependencies"
```

#### Initialize Admin Account
```
Ctrl+Shift+P → "Tasks: Run Task" → "Initialize Admin"
```

#### Build for Production
```
Ctrl+Shift+P → "Tasks: Run Task" → "frontend: build"
```

---

## ⌨️ Keyboard Shortcuts

### Essential Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| **Start Debugging** | `F5` | `F5` |
| **Command Palette** | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| **Quick Open File** | `Ctrl+P` | `Cmd+P` |
| **Toggle Terminal** | `Ctrl+`` | `Ctrl+`` |
| **Format Document** | `Shift+Alt+F` | `Shift+Option+F` |
| **Toggle Breakpoint** | `F9` | `F9` |
| **Search All Files** | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| **Toggle Sidebar** | `Ctrl+B` | `Cmd+B` |

### Debugging Shortcuts

| Action | Shortcut |
|--------|----------|
| Continue | `F5` |
| Step Over | `F10` |
| Step Into | `F11` |
| Step Out | `Shift+F11` |
| Toggle Breakpoint | `F9` |
| Stop Debugging | `Shift+F5` |

---

## 🌐 Access Your Application

Once running:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api
- **Admin Login**: 
  - Email: `admin@eventmanagement.com`
  - Password: `Admin@12345`

---

## 🛠️ First Time Setup

### 1. Install Dependencies
Run task: **"Install All Dependencies"**

Or manually:
```bash
cd backend && npm install
cd ../frontend && npm install
```

### 2. Configure Environment Variables

**Backend** (`backend/.env`):
```bash
cd backend
cp .env.example .env
# Edit .env with your settings
```

**Frontend** (`frontend/.env`):
```bash
cd frontend
cp .env.example .env
# Usually default settings work
```

### 3. Start MongoDB
Make sure MongoDB is running:
```bash
# Mac (Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Windows
net start MongoDB
```

Or use **MongoDB Atlas** (cloud):
- Update `MONGODB_URI` in `backend/.env`

### 4. Initialize Admin Account
Run task: **"Initialize Admin"**

Or:
```bash
curl -X POST http://localhost:5000/api/admin/init
```

### 5. Start Development!
Press `F5` → Select "Run Full Stack" → Happy coding! 🎉

---

## 📚 Documentation Files

- **VSCODE_GUIDE.md** - Comprehensive VS Code guide (10KB+)
- **.vscode/README.md** - Quick reference card
- **QUICKSTART.md** - API documentation and quick start
- **README_MERN.md** - Project overview
- **assignment1.md** - Assignment requirements

---

## 🔍 Project Structure in VS Code

```
📁 Megathon_Project/
├── 📁 .vscode/                   👈 VS Code configuration
│   ├── launch.json               → Debug configurations
│   ├── tasks.json                → Task definitions
│   ├── settings.json             → Workspace settings
│   ├── extensions.json           → Recommended extensions
│   └── README.md                 → Quick reference
├── 📁 backend/                   👈 Express.js API
│   ├── 📁 models/                → Database schemas
│   ├── 📁 routes/                → API endpoints
│   ├── 📁 middleware/            → Auth & validation
│   ├── 📁 utils/                 → Helper functions
│   └── server.js                 → Entry point
├── 📁 frontend/                  👈 React application
│   └── 📁 src/
│       ├── 📁 components/        → Reusable components
│       ├── 📁 pages/             → Page components
│       ├── 📁 contexts/          → React contexts
│       ├── 📁 services/          → API services
│       └── App.jsx               → Main component
├── 📄 VSCODE_GUIDE.md            👈 Complete VS Code guide
├── 📄 Megathon_Project.code-workspace  → Multi-root workspace
└── 📄 start-dev.sh               → Bash startup script
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

### MongoDB Not Running
```bash
# Check if MongoDB is running
mongosh

# Start MongoDB
brew services start mongodb-community  # Mac
sudo systemctl start mongod            # Linux
```

### Extensions Not Working
1. Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"
2. Check extension panel for errors
3. Reinstall problematic extension

### Debugger Not Attaching
1. Make sure server is running
2. Check port numbers match in `launch.json`
3. Try "Backend: Attach" configuration
4. Restart VS Code

### ESLint Errors
1. Install dependencies: `npm install`
2. Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"
3. Check ESLint output: View → Output → Select "ESLint"

---

## 💡 Pro Tips

### Multi-Root Workspace
Open the workspace file for better organization:
```
File → Open Workspace from File → Select Megathon_Project.code-workspace
```

This creates separate folders for backend and frontend in the sidebar!

### Terminal Shortcuts
- **New Terminal**: `` Ctrl+Shift+` ``
- **Split Terminal**: `Ctrl+Shift+5`
- **Switch Terminal**: `Ctrl+PageUp/PageDown`

### Useful Extensions (Already Recommended)
- **MongoDB for VS Code** - Browse and query your database
- **Error Lens** - See errors inline
- **Import Cost** - See package sizes
- **Better Comments** - Colorful comments

### Code Snippets
With ES7+ React snippets installed:
- Type `rafce` → React Arrow Function Component
- Type `useState` → React useState hook
- Type `useEffect` → React useEffect hook

---

## ✅ Verification Checklist

Before you start coding, ensure:
- [ ] VS Code installed
- [ ] Project opened in VS Code
- [ ] Recommended extensions installed
- [ ] Dependencies installed (`npm install` in both folders)
- [ ] Environment files configured (`.env`)
- [ ] MongoDB running (local or Atlas)
- [ ] Admin account initialized
- [ ] Can press F5 and see both servers start

---

## 🎓 Learning Resources

### VS Code
- [Keyboard Shortcuts PDF](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
- [Tips and Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)

### Debugging
- [Debugging Guide](https://code.visualstudio.com/docs/editor/debugging)
- [Node.js Debugging](https://code.visualstudio.com/docs/nodejs/nodejs-debugging)

### This Project
- `VSCODE_GUIDE.md` - Detailed VS Code instructions
- `QUICKSTART.md` - API documentation
- `README_MERN.md` - Project overview

---

## 🎉 You're All Set!

Your development environment is now **fully configured** with:
- ✅ One-click debugging
- ✅ Automated tasks
- ✅ Code formatting
- ✅ Linting
- ✅ Intelligent autocomplete
- ✅ Hot module replacement
- ✅ Git integration

### Next Step: Start Coding!

1. Press `F5`
2. Select "Run Full Stack"
3. Open http://localhost:5173
4. Start building amazing features! 🚀

**Happy Coding!** 💻✨
