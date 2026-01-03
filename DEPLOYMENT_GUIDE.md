# 🚀 Deployment Guide - Movie & Book Recommender

## Overview
- **Frontend**: React + Vite → Vercel
- **Backend**: FastAPI + Python → Render/Railway/Fly.io

---

## 📱 Frontend Deployment (Vercel)

### Option 1: Deploy via Vercel Dashboard (Easiest)
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your repository
5. Set these settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `movie-recommender-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add Environment Variable:
   - `VITE_API_URL` = `https://your-backend-url.onrender.com`
7. Click "Deploy"

### Option 2: Deploy via Vercel CLI
```bash
cd movie-recommender-frontend
npm install -g vercel
vercel login
vercel --prod
```

### Update API URL in Production
Before deploying, update `App.jsx`:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

---

## 🔧 Backend Deployment Options

### Option 1: Render (Recommended - Free Tier) ⭐

#### Steps:
1. **Push to GitHub**
   ```bash
   cd C:\Users\Admin\Desktop\movie_eccomender
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/movie-book-recommender.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Name**: movie-book-recommender-api
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free
   - Click "Create Web Service"

3. **Note**: Free tier sleeps after 15 min of inactivity (first request may be slow)

4. **Copy your Render URL** (e.g., `https://movie-book-recommender-api.onrender.com`)

#### Important: Update CORS in main.py
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-vercel-app.vercel.app",  # Add your Vercel URL
        "*"  # For testing only, remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Option 2: Railway (Easiest Setup)

#### Steps:
1. **Push to GitHub** (same as above)

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and uses `railway.toml`
   - Click "Deploy"

3. **Add Domain**
   - Go to Settings → Generate Domain
   - Copy the URL

4. **Cost**: Free $5 credit, then $5/month

---

### Option 3: Fly.io (Developer-Friendly)

#### Steps:
1. **Install Fly CLI**
   ```bash
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login and Deploy**
   ```bash
   cd C:\Users\Admin\Desktop\movie_eccomender
   fly auth login
   fly launch
   ```
   
3. **Follow prompts**:
   - App name: movie-book-recommender
   - Region: Choose nearest
   - PostgreSQL: No
   - Redis: No

4. **Deploy**:
   ```bash
   fly deploy
   ```

---

### Option 4: PythonAnywhere (Python-Specific)

#### Steps:
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload your files via Files tab
3. Create a new Web app → Manual configuration → Python 3.10
4. Configure WSGI file:
   ```python
   from main import app as application
   ```
5. Set working directory to your app folder
6. Reload web app

---

## 🔒 Environment Variables

### Backend (.env file)
```env
TMDB_API_KEY=8265bd1679663a7ea12ac168da84d2e8
```

### Frontend (.env file in movie-recommender-frontend/)
```env
VITE_API_URL=https://your-backend-url.com
```

---

## 📦 File Size Considerations

Your pickle files are:
- `movie_list.pkl` - Small
- `similarity.pkl` - ~90MB (large!)
- `book_pivot.pkl` - Small
- `book_similarity.pkl` - ~4MB
- `popular_books.pkl` - Small

⚠️ **Important**: Some free tiers have file size limits:
- Render Free: 512MB total (should be fine)
- Railway: 1GB (no issue)
- Fly.io: 500MB per app (should work)

If `similarity.pkl` is too large, consider:
1. Using Git LFS (Large File Storage)
2. Storing on cloud storage (S3/Cloudflare R2)
3. Reducing matrix precision (float32 → float16)

---

## 🔗 Connecting Frontend to Backend

After deploying backend, update frontend API URL:

**In `movie-recommender-frontend/src/App.jsx`:**
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'https://your-backend-url.onrender.com';
```

**Create `.env` file in `movie-recommender-frontend/`:**
```env
VITE_API_URL=https://your-backend-url.onrender.com
```

Then redeploy frontend on Vercel.

---

## ✅ Deployment Checklist

### Before Deployment:
- [ ] Push code to GitHub
- [ ] Ensure all pickle files are committed
- [ ] Update CORS origins in `main.py`
- [ ] Test locally: `uvicorn main:app --reload`

### Backend Deployment:
- [ ] Deploy to Render/Railway/Fly.io
- [ ] Test API endpoints: `/`, `/docs`
- [ ] Copy backend URL

### Frontend Deployment:
- [ ] Update `VITE_API_URL` environment variable
- [ ] Deploy to Vercel
- [ ] Test both Movies and Books tabs
- [ ] Verify recommendations work

---

## 🐛 Troubleshooting

### CORS Errors
Add your Vercel URL to `allow_origins` in `main.py`:
```python
allow_origins=["https://your-app.vercel.app", "*"]
```

### API Not Loading
- Check backend logs on hosting platform
- Verify `PORT` environment variable is used
- Check if pickle files uploaded correctly

### Slow First Request (Render)
- Free tier sleeps after 15 min
- First request wakes it up (~30s delay)
- Upgrade to paid tier for always-on

### Large File Issues
- Use Git LFS for files >100MB
- Or split into smaller chunks

---

## 💰 Cost Summary

| Service | Free Tier | Paid |
|---------|-----------|------|
| **Vercel** | 100GB bandwidth | $20/month |
| **Render** | 750 hrs/month, sleeps | $7/month always-on |
| **Railway** | $5 credit | $5/month usage-based |
| **Fly.io** | 3 VMs, 160GB | Pay as you go |

**Recommendation**: Start with Render (backend) + Vercel (frontend) - Both FREE! 🎉

---

## 📚 Quick Deploy Commands

```bash
# Backend to Render
git init
git add .
git commit -m "Deploy backend"
git push

# Frontend to Vercel
cd movie-recommender-frontend
vercel --prod
```

---

## 🎉 Done!

Your app should now be live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-api.onrender.com`
- **API Docs**: `https://your-api.onrender.com/docs`

Need help? Check the logs on your hosting platform!
