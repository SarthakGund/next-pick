# Quick GitHub Push Guide

## ⚠️ First: Restart PowerShell to use Git

Close this PowerShell window and open a NEW one, then:

## Step 1: Configure Git
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 2: Initialize & Commit
```powershell
cd C:\Users\Admin\Desktop\movie_eccomender
git init
git add .
git commit -m "Initial commit: Movie & Book Recommender System"
```

## Step 3: Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `movie-book-recommender` (or your choice)
3. Description: "AI-powered movie and book recommendation system"
4. **DON'T** initialize with README (we already have files)
5. Click "Create repository"

## Step 4: Push to GitHub
```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Step 5: Deploy Backend (Render)
1. Go to: https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - **Name**: movie-book-api
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Copy your Render URL (e.g., `https://movie-book-api.onrender.com`)

## Step 6: Deploy Frontend (Vercel)
1. Go to: https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `movie-recommender-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - Name: `VITE_API_URL`
   - Value: `https://your-render-url.onrender.com` (from step 5)
6. Click "Deploy"

## Step 7: Update CORS in main.py
After deployment, add your Vercel URL to the CORS origins:
```python
allow_origins=[
    "http://localhost:5173",
    "https://your-app.vercel.app",  # Add this
    "*"  # Remove this in production
],
```

## ✅ Done!
Your app will be live at:
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-api.onrender.com`
- API Docs: `https://your-api.onrender.com/docs`

---

## 📦 What Gets Pushed:
✅ Backend code (`main.py`, `requirements.txt`)
✅ All `.pkl` model files (~100MB)
✅ Frontend code (React app)
✅ Documentation files

❌ `venv/`, `node_modules/` (ignored)
❌ `.csv` files (ignored)
❌ `.ipynb` notebooks (ignored)
