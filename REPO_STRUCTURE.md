# 📦 Git Repository Structure

## ✅ Files that WILL be pushed to GitHub (Essential):

### Backend (Root)
- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `*.pkl` files - Pre-trained models (MUST INCLUDE!)
  - `movie_list.pkl` (~2MB)
  - `similarity.pkl` (~90MB) ⚠️ Large file
  - `book_pivot.pkl` (~500KB)
  - `book_similarity.pkl` (~4MB)
  - `popular_books.pkl` (~100KB)

### Frontend
- `movie-recommender-frontend/src/` - React components
- `movie-recommender-frontend/package.json` - Dependencies
- `movie-recommender-frontend/vite.config.js` - Vite config
- `movie-recommender-frontend/index.html`
- `movie-recommender-frontend/tailwind.config.js`
- `movie-recommender-frontend/.env.example` - Example env file

### Documentation
- `README.md` - Project overview
- `DEPLOYMENT_GUIDE.md` - How to deploy
- `API_GUIDE.md` - API documentation

### Config Files
- `.gitignore` - Git ignore rules

---

## ❌ Files that will NOT be pushed (Excluded by .gitignore):

### Python Environment
- `venv/`, `.venv/` - Virtual environments (huge!)
- `__pycache__/` - Python cache files
- `*.pyc` - Compiled Python

### Data Files (Not needed in production)
- `*.csv` - Raw CSV data files
  - `Books.csv`
  - `Ratings.csv`
  - `Users.csv`
  - `tmdb_5000_movies.csv`
  - `tmdb_5000_credits.csv`

### Jupyter Notebooks
- `*.ipynb` - Notebook files (development only)
  - `book-recommender-system.ipynb`
  - `movie-recommender-system.ipynb`

### Frontend Build Files
- `movie-recommender-frontend/node_modules/` - Dependencies (huge!)
- `movie-recommender-frontend/dist/` - Build output
- `movie-recommender-frontend/.env` - Local env vars

### Test & Setup Files
- `test_api.py` - Local testing script
- `setup-frontend.ps1` - Local setup script
- `App.jsx.template` - Template file

### Environment Files
- `.env` - Environment variables (secrets!)

---

## 📊 Size Breakdown:

**What gets pushed:** ~100MB
- Pickle files: ~96MB
- Source code: ~4MB

**What stays local:** ~2GB+
- `node_modules/`: ~500MB
- `venv/`: ~1GB
- CSV files: ~200MB
- Jupyter notebooks: ~50MB

---

## ⚠️ Important Notes:

### Large File Warning
Your `similarity.pkl` (~90MB) is close to GitHub's 100MB limit.

**Options:**
1. **Keep as-is** - Should work fine (under 100MB)
2. **Git LFS** - Use for files >50MB (safer)
3. **Cloud Storage** - Store on S3/Cloudflare R2 and download on deploy

### To Use Git LFS (if needed):
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
```

---

## 🚀 Deployment Note:

The pickle files MUST be pushed to GitHub because:
- Render/Railway/Vercel clone from GitHub
- Your app needs these models to run
- They're pre-computed (can't regenerate without CSV data)

---

## ✅ What to do next:

1. Review `.gitignore` - All set!
2. Initialize git:
   ```bash
   git init
   git add .
   git status  # Verify only essential files are staged
   git commit -m "Initial commit: Movie & Book Recommender"
   ```
3. Check file size:
   ```bash
   git ls-files -s | awk '{sum+=$4} END {print sum/1024/1024 " MB"}'
   ```
4. Push to GitHub!
