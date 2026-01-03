# Movie Recommender System

A content-based movie recommendation system using machine learning and cosine similarity.

## Architecture

- **Backend:** Flask REST API (Python)
- **Frontend:** React (JavaScript)
- **ML Model:** Content-based filtering with TF-IDF and Cosine Similarity

## Setup Instructions

### 1. First, save the model data from Jupyter Notebook

Run the last cell in `movie-recommender-system.ipynb` to generate:
- `movie_list.pkl`
- `similarity.pkl`

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Flask API

```bash
python api.py
```

API will run at `http://localhost:5000`

### 4. Setup React Frontend

```bash
cd movie-recommender-frontend
npm install
npm start
```

React app will run at `http://localhost:3000`

## API Endpoints

### GET /api/movies
Returns list of all movies
```json
{
  "success": true,
  "movies": ["Avatar", "Spectre", ...],
  "count": 4809
}
```

### POST /api/recommend
Get movie recommendations
```json
// Request
{
  "movie": "Avatar"
}

// Response
{
  "success": true,
  "movie": "Avatar",
  "recommendations": ["Movie1", "Movie2", ...]
}
```

## Tech Stack

### Backend
- Flask - Web framework
- Flask-CORS - Handle cross-origin requests
- Pandas - Data manipulation
- Scikit-learn - Machine learning
- Pickle - Model serialization

### Frontend
- React - UI library
- Axios - HTTP client
- CSS - Styling
