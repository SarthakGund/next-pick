# Movie Recommender - Setup Guide

## Step 1: Install Backend Dependencies

```powershell
cd C:\Users\Admin\Desktop\movie_eccomender
pip install fastapi uvicorn pydantic pandas numpy scikit-learn
```

## Step 2: Save Model Data (Run Notebook Cell)

Make sure to run the notebook cell that saves the pickle files:
```python
import pickle
pickle.dump(new_df, open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
```

## Step 3: Start FastAPI Backend

```powershell
cd C:\Users\Admin\Desktop\movie_eccomender
uvicorn main:app --reload
```

Backend will run at: http://localhost:8000
API docs at: http://localhost:8000/docs

## Step 4: Create React Frontend with Vite + Tailwind

### 4.1: Create React App
```powershell
# In a NEW terminal window
cd C:\Users\Admin\Desktop\movie_eccomender
npm create vite@latest movie-recommender-frontend -- --template react
```

When prompted about existing directory, choose "Remove existing files and continue"

### 4.2: Install Dependencies
```powershell
cd movie-recommender-frontend
npm install
npm install axios
```

### 4.3: Install Tailwind CSS
```powershell
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 4.4: Configure Tailwind

Edit `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 4.5: Add Tailwind to CSS

Replace content of `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Step 5: Run React Frontend

```powershell
npm run dev
```

Frontend will run at: http://localhost:5173

## Testing

1. Backend: http://localhost:8000/docs
2. Frontend: http://localhost:5173
3. Select a movie and get recommendations!

## Architecture

```
React (Port 5173)
    ↓ HTTP Request
FastAPI (Port 8000)
    ↓ Load Data
Pickle Files (movie_list.pkl, similarity.pkl)
```
