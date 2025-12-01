# Resume Chatbot Deployment Guide

This guide covers deploying both the frontend (to GitHub Pages) and backend (to Railway).

## Frontend Deployment (GitHub Pages)

### Prerequisites
1. GitHub repository set up
2. Node.js and npm installed

### Steps
1. **Build the project:**
   ```bash
   npm run build:gh-pages
   ```

2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Deploy to GitHub Pages"
   git push origin main
   ```

3. **Configure GitHub Pages:**
   - Go to your repository Settings
   - Navigate to Pages section
   - Under Source, select "Deploy from a branch"
   - Choose `main` branch and `/docs` folder
   - Save settings

Your frontend will be available at: `https://yourusername.github.io/resume-chatbot-ui/`

## Backend Deployment (Railway)

### Prerequisites
1. Railway account (https://railway.app)
2. OpenRouter API key

### Steps
1. **Create new Railway project:**
   - Connect your GitHub repository
   - Set root directory to `resume_backend`
   - Railway will detect it as a Python project due to requirements.txt and Dockerfile

2. **Configure environment variables:**
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `PORT`: Will be set automatically by Railway

3. **Deploy:**
   - Railway will automatically deploy when you push to main branch
   - Uses the Dockerfile in resume_backend/ for containerized deployment
   - Note your Railway URL (e.g., `https://your-app.railway.app`)

4. **Update frontend WebSocket URL:**
   - Replace `'your-railway-app.railway.app'` in `src/pages/chat/chat.tsx`
   - With your actual Railway URL

### Alternative Deployment Options

#### Render
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python main.py`
4. Add environment variables

#### Heroku
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Set environment variables: `heroku config:set OPENROUTER_API_KEY=your-key`
4. Deploy: `git push heroku main`

## Environment Variables

### Frontend (.env)
```
VITE_WEBSOCKET_URL=ws://localhost:8765
VITE_PRODUCTION_WEBSOCKET_URL=wss://your-railway-app.railway.app
```

### Backend (Railway/Heroku)
```
OPENROUTER_API_KEY=your-openrouter-api-key
PORT=8765 (set automatically by hosting platform)
```

## Local Development

### Frontend
```bash
npm install
npm run dev
```

### Backend
```bash
cd resume_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Troubleshooting

### Common Issues
1. **WebSocket connection failed:** Check that backend is deployed and URL is correct
2. **Build fails:** Ensure all dependencies are installed with `npm ci`
3. **CORS issues:** Backend automatically handles CORS for WebSocket connections
4. **OpenRouter API errors:** Check API key and quota

### Debugging
- Check browser console for frontend errors
- Check Railway logs for backend errors
- Verify environment variables are set correctly
