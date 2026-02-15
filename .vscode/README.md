# 🚀 VS Code Quick Reference

## Run the Project

### Option 1: Debug Configuration (Recommended)
1. Press `F5` or click Debug icon
2. Select "**Run Full Stack**" from dropdown
3. Both backend and frontend will start!

### Option 2: Using Tasks
1. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
2. Type "Tasks: Run Task"
3. Select "Run Full Stack"

### Option 3: Terminal Commands
```bash
# Backend
cd backend && npm run dev

# Frontend (new terminal)
cd frontend && npm run dev
```

## First Time Setup

1. **Install Extensions**
   - VS Code will prompt you - click "Install All"

2. **Install Dependencies**
   - Run Task: "Install All Dependencies"
   - Or: `npm install` in both backend and frontend folders

3. **Set Up Environment**
   ```bash
   cd backend && cp .env.example .env
   cd ../frontend && cp .env.example .env
   ```

4. **Initialize Admin**
   - Run Task: "Initialize Admin"
   - Or: `curl -X POST http://localhost:5000/api/admin/init`

## Access Points

- 🌐 Frontend: http://localhost:5173
- 🔧 Backend: http://localhost:5000/api
- 👤 Admin: admin@eventmanagement.com / Admin@12345

## Keyboard Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Run/Debug | `F5` | `F5` |
| Open Command Palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Toggle Terminal | `Ctrl+`` | `Ctrl+`` |
| Quick Open File | `Ctrl+P` | `Cmd+P` |
| Format Document | `Shift+Alt+F` | `Shift+Option+F` |
| Toggle Breakpoint | `F9` | `F9` |

## Debugging

1. Set breakpoints by clicking left of line numbers
2. Select debug configuration (Backend/Frontend/Full Stack)
3. Press `F5` to start
4. Use debug controls to step through code

## Tasks Available

- **Install All Dependencies** - Setup project
- **Run Full Stack** - Start both servers
- **backend: dev** - Start backend only
- **frontend: dev** - Start frontend only
- **frontend: build** - Build for production
- **Initialize Admin** - Create admin account

## Common Issues

**Port in use?**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

**MongoDB not running?**
```bash
# Start MongoDB
brew services start mongodb-community  # Mac
sudo systemctl start mongod            # Linux
```

**Need more help?**
- See `VSCODE_GUIDE.md` for detailed instructions
- See `QUICKSTART.md` for API documentation

---

**Pro Tip:** Open the workspace file (`Megathon_Project.code-workspace`) for better folder organization!
