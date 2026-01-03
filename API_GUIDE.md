# Movie & Book Recommender API Guide

## Overview
Unified FastAPI backend serving both movie and book recommendations.

## Server
- **Base URL**: `http://localhost:8000`
- **Documentation**: `http://localhost:8000/docs` (Interactive Swagger UI)
- **Start command**: `uvicorn main:app --reload`

## API Endpoints

### Movies

#### 1. Get All Movies
```http
GET /api/movies
```
Returns list of all 4,806 available movies.

#### 2. Get Movie Recommendations
```http
POST /api/recommend
Content-Type: application/json

{
  "movie": "Avatar",
  "count": 5
}
```
Returns content-based recommendations for the specified movie.

**Response:**
```json
{
  "success": true,
  "movie": "Avatar",
  "recommendations": [
    {
      "title": "Aliens",
      "poster_url": null,
      "tmdb_id": null
    }
  ]
}
```

### Books

#### 1. Get All Books
```http
GET /api/books
```
Returns list of all 707 books available for collaborative filtering.

#### 2. Get Popular Books
```http
GET /api/books/popular
```
Returns top 100 popular books with ratings and metadata.

**Response:**
```json
{
  "success": true,
  "count": 100,
  "books": [
    {
      "title": "Harry Potter and the Prisoner of Azkaban (Book 3)",
      "author": "J. K. Rowling",
      "image_url": "http://images.amazon.com/...",
      "avg_rating": 5.85,
      "num_ratings": 550
    }
  ]
}
```

#### 3. Get Book Recommendations
```http
POST /api/books/recommend
Content-Type: application/json

{
  "book": "1984",
  "count": 5
}
```
Returns collaborative filtering-based recommendations for the specified book.

**Response:**
```json
{
  "success": true,
  "book": "1984",
  "recommendations": [
    {
      "title": "Animal Farm",
      "author": "George Orwell",
      "image_url": "http://images.amazon.com/...",
      "avg_rating": 4.8,
      "num_ratings": 320
    }
  ]
}
```

## Recommendation Algorithms

### Movies
- **Type**: Content-Based Filtering
- **Features**: Genre, keywords, cast, crew
- **Similarity**: Cosine similarity on TF-IDF vectors
- **Dataset**: TMDB 5000 Movie Dataset

### Books
- **Type**: Collaborative Filtering
- **Method**: User-based similarity
- **Similarity**: Cosine similarity on user-item matrix
- **Dataset**: Book-Crossings Dataset
- **Filter**: Users with ≥200 ratings, Books with ≥50 ratings

## Model Files

### Movies
- `movie_list.pkl` - DataFrame with 4,806 movies
- `similarity.pkl` - 4806×4806 similarity matrix

### Books
- `book_pivot.pkl` - 707×815 pivot table (books × users)
- `book_similarity.pkl` - 707×707 similarity matrix
- `popular_books.pkl` - Top 100 popular books DataFrame

## Testing

Run the test script:
```bash
python test_api.py
```

## CORS Configuration
Configured to accept requests from:
- `http://localhost:5174` (Vite)
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (React)

## Next Steps for Frontend Integration

1. **Create Book Recommendation UI** similar to movie UI
2. **Add Navigation** to switch between Movies and Books
3. **Display Popular Books** as initial view
4. **Implement Book Search** with autocomplete
5. **Show Book Details** including cover images, author, ratings

### Example Frontend API Calls

```javascript
// Get popular books
const response = await axios.get('http://localhost:8000/api/books/popular');

// Get book recommendations
const response = await axios.post('http://localhost:8000/api/books/recommend', {
  book: '1984',
  count: 10
});

// Get movie recommendations
const response = await axios.post('http://localhost:8000/api/recommend', {
  movie: 'Avatar',
  count: 10
});
```

## Statistics
- ✓ 4,806 Movies loaded
- ✓ 707 Books for collaborative filtering
- ✓ 100 Popular books precomputed
- ✓ Single unified backend (one server to host)
