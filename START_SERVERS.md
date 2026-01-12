# Starting PolicyIQ Servers

## Quick Start

You need to run **both** the backend and frontend servers for PolicyIQ to work.

### Terminal 1: Backend Server

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Backend will be available at:** http://localhost:8000
**API Documentation:** http://localhost:8000/docs

### Terminal 2: Frontend Server

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/frontend
npm start
```

The browser should automatically open to http://localhost:3000

## Troubleshooting

### Proxy Error: ECONNREFUSED

**Error:** `Proxy error: Could not proxy request from localhost:3000 to http://localhost:8000`

**Cause:** The backend server is not running.

**Solution:**
1. Make sure you've started the backend server (Terminal 1)
2. Verify it's running on port 8000:
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy"}`

3. If the backend isn't running, start it:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --port 8000
   ```

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
- Find what's using the port:
  ```bash
  lsof -i :8000  # For backend
  lsof -i :3000  # For frontend
  ```
- Kill the process or use a different port:
  ```bash
  # Backend on different port
  uvicorn main:app --reload --port 8001
  
  # Then update frontend/src/services/api.js
  # Change API_BASE_URL to use port 8001
  ```

### Backend Won't Start

**Check:**
1. Virtual environment is activated: `which python` should show venv path
2. Dependencies installed: `pip list | grep fastapi`
3. .env file exists: `ls backend/.env`
4. No syntax errors: `python -m py_compile backend/main.py`

### Frontend Won't Start

**Check:**
1. Node modules installed: `ls frontend/node_modules`
2. If missing: `cd frontend && npm install`
3. Port 3000 available: `lsof -i :3000`

## Verification

Once both servers are running:

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Frontend:**
   - Open http://localhost:3000
   - Should see PolicyIQ navigation (Chat, Upload, Audit Logs)

3. **API Docs:**
   - Open http://localhost:8000/docs
   - Should see Swagger UI with all endpoints

## Development Workflow

1. **Start Backend** (Terminal 1) - Keep it running
2. **Start Frontend** (Terminal 2) - Keep it running
3. **Make Changes** - Both servers auto-reload on file changes
4. **Test** - Use the frontend UI or API docs

## Stopping Servers

- **Backend:** Press `Ctrl+C` in Terminal 1
- **Frontend:** Press `Ctrl+C` in Terminal 2

## Common Issues

### "Module not found" errors
- Backend: Make sure venv is activated and dependencies installed
- Frontend: Run `npm install` in frontend directory

### CORS errors
- Backend CORS is configured for localhost:3000
- If using different port, update `backend/main.py` CORS settings

### API calls failing
- Check backend is running
- Check browser console for errors
- Verify API_BASE_URL in `frontend/src/services/api.js`
