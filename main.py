"""
Movie & Book Recommender API using FastAPI

FastAPI is a modern Python web framework for building APIs.
It's faster than Flask and has automatic documentation.
"""

# ============= IMPORTS =============
# FastAPI: The main framework for creating the API
from fastapi import FastAPI, HTTPException
# CORSMiddleware: Allows React (different port) to access this API
from fastapi.middleware.cors import CORSMiddleware
# BaseModel: Used to define the structure of data we receive/send
from pydantic import BaseModel
# Standard libraries
import pickle
import pandas as pd
import numpy as np
from typing import List, Optional
import requests

# ============= INITIALIZE APP =============
# Create a FastAPI application instance
app = FastAPI(
    title="Movie & Book Recommender API",
    description="API for getting movie and book recommendations based on content similarity",
    version="2.0.0"
)

# ============= CORS CONFIGURATION =============
"""
CORS = Cross-Origin Resource Sharing

Problem: By default, browsers block requests between different origins (ports)
- React runs on: http://localhost:3000
- FastAPI runs on: http://localhost:8000
- Browser sees these as different origins and blocks requests

Solution: Tell FastAPI to allow requests from React's origin
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174", 
        "http://localhost:5173", 
        "http://localhost:3000",
        "https://next-pick.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ============= TMDB API CONFIGURATION =============
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# ============= LOAD MODEL DATA =============
"""
Load the pickle files we created in the notebook
These files contain:

MOVIES:
1. movie_list.pkl: DataFrame with movie_id, title, and tags
2. similarity.pkl: 2D array of similarity scores between all movies

BOOKS:
1. book_pivot.pkl: Pivot table with books as index and users as columns
2. book_similarity.pkl: 2D array of similarity scores between all books
3. popular_books.pkl: Top 100 popular books with ratings
"""
print("Loading movie data...")
movies_df = pickle.load(open('movie_list.pkl', 'rb'))
similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
print(f"✓ Loaded {len(movies_df)} movies")

print("Loading book data...")
book_pivot = pickle.load(open('book_pivot.pkl', 'rb'))
book_similarity = pickle.load(open('book_similarity.pkl', 'rb'))
popular_books = pickle.load(open('popular_books.pkl', 'rb'))
print(f"✓ Loaded {len(book_pivot.index)} books for collaborative filtering")
print(f"✓ Loaded {len(popular_books)} popular books")

# ============= DATA MODELS (Schemas) =============
"""
Pydantic models define the structure of data
This is like a contract: "Data must look like this"

Benefits:
- Automatic validation: FastAPI checks if data matches
- Auto documentation: Shows in API docs
- Type safety: Catches errors early
"""

class RecommendationRequest(BaseModel):
    """
    This defines what data we expect when someone asks for recommendations
    Example: {"movie": "Avatar", "count": 10}
    """
    movie: str  # Movie name as a string
    count: int = 5  # Number of recommendations (default 5, max 20)
    
    class Config:
        # Example shown in API documentation
        schema_extra = {
            "example": {
                "movie": "The Dark Knight",
                "count": 5
            }
        }

class BookRecommendationRequest(BaseModel):
    """
    Request model for book recommendations
    """
    book: str  # Book title
    count: int = 5  # Number of recommendations (default 5)
    
    class Config:
        schema_extra = {
            "example": {
                "book": "1984",
                "count": 5
            }
        }

class MovieRecommendation(BaseModel):
    """
    Single movie recommendation with poster
    """
    title: str
    poster_url: Optional[str] = None
    tmdb_id: Optional[int] = None

class BookRecommendation(BaseModel):
    """
    Single book recommendation
    """
    title: str
    author: str
    image_url: Optional[str] = None
    avg_rating: Optional[float] = None
    num_ratings: Optional[int] = None

class RecommendationResponse(BaseModel):
    """
    This defines what we send back for movie recommendations
    """
    success: bool
    movie: str
    recommendations: List[MovieRecommendation]  # List of movie titles

class BookRecommendationResponse(BaseModel):
    """
    Response for book recommendations
    """
    success: bool
    book: str
    recommendations: List[BookRecommendation]

class MoviesResponse(BaseModel):
    """
    Response when fetching all movies
    """
    success: bool
    count: int
    movies: List[str]

class BooksResponse(BaseModel):
    """
    Response when fetching all books
    """
    success: bool
    count: int
    books: List[str]

class PopularBooksResponse(BaseModel):
    """
    Response for popular books
    """
    success: bool
    count: int
    books: List[BookRecommendation]

# ============= HELPER FUNCTIONS =============
def fetch_poster_from_tmdb(movie_title: str, movie_id: int = None) -> Optional[str]:
    """
    Fetch movie poster from TMDB API
    
    Args:
        movie_title: Title of the movie
        movie_id: TMDB movie ID if available
    
    Returns:
        Full URL to poster image or None if not found
    """
    try:
        # Search for movie by title
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title
        }
        
        # Quick timeout - fail fast if TMDB is having issues
        response = requests.get(search_url, params=params, timeout=2, verify=False)
        response.raise_for_status()
        data = response.json()
        
        if data['results']:
            # Get the first result (most relevant)
            poster_path = data['results'][0].get('poster_path')
            tmdb_id = data['results'][0].get('id')
            
            if poster_path:
                return f"{TMDB_IMAGE_BASE_URL}{poster_path}", tmdb_id
        
        return None, None
    except requests.exceptions.Timeout:
        print(f"Timeout fetching poster for {movie_title}")
        return None, None
    except requests.exceptions.ConnectionError:
        print(f"Connection error for {movie_title}")
        return None, None
    except Exception as e:
        print(f"Error fetching poster for {movie_title}: {e}")
        return None, None

def get_recommendations(movie_title: str, top_n: int = 5) -> List[MovieRecommendation]:
    """
    Core recommendation function - returns movie titles
    
    Args:
        movie_title: Name of the movie to base recommendations on
        top_n: Number of recommendations to return (default 5, max 20)
    
    Returns:
        List of MovieRecommendation objects with titles
    
    How it works:
    1. Find the index of the selected movie in our dataframe
    2. Get similarity scores for this movie with all others
    3. Sort by similarity (highest first)
    4. Skip first one (the movie itself) and take top N
    5. Return the movie titles
    """    # Enforce maximum limit
    top_n = min(top_n, 20)
        # Enforce maximum limit
    top_n = min(top_n, 20)
    # Find the movie's index
    # This will raise an error if movie not found
    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    
    # Get similarity scores for this movie
    # similarity_matrix[movie_index] gives us an array of scores
    distances = similarity_matrix[movie_index]
    
    # Create list of (index, similarity_score) tuples
    # enumerate() gives us both position and value
    movies_list = list(enumerate(distances))
    
    # Sort by similarity score (highest first)
    # key=lambda x: x[1] means sort by the second element (the score)
    # reverse=True means highest first
    movies_list_sorted = sorted(movies_list, reverse=True, key=lambda x: x[1])
    
    # Skip first movie (itself) and take next top_n
    top_movies = movies_list_sorted[1:top_n+1]
    
    # Extract movie titles (skipping posters for now)
    recommendations = []
    for i in top_movies:
        movie_title = movies_df.iloc[i[0]].title
        recommendations.append(MovieRecommendation(
            title=movie_title,
            poster_url=None,
            tmdb_id=None
        ))
    
    return recommendations

def get_book_recommendations(book_title: str, top_n: int = 5) -> List[BookRecommendation]:
    """
    Core book recommendation function
    
    Args:
        book_title: Name of the book to base recommendations on
        top_n: Number of recommendations to return
    
    Returns:
        List of BookRecommendation objects
    """
    # Enforce maximum limit
    top_n = min(top_n, 20)
    
    # Find the book's index in pivot table
    if book_title not in book_pivot.index:
        raise ValueError(f"Book '{book_title}' not found in database")
    
    book_index = np.where(book_pivot.index == book_title)[0][0]
    
    # Get similarity scores for this book
    distances = book_similarity[book_index]
    
    # Create list of (index, similarity_score) tuples
    similar_items = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:top_n+1]
    
    # Extract book recommendations
    recommendations = []
    for i in similar_items:
        book_name = book_pivot.index[i[0]]
        
        # Try to get additional info from popular_books if available
        book_info = popular_books[popular_books['Book-Title'] == book_name]
        
        if len(book_info) > 0:
            book_data = book_info.iloc[0]
            recommendations.append(BookRecommendation(
                title=book_name,
                author=book_data['Book-Author'],
                image_url=book_data['Image-URL-M'],
                avg_rating=float(book_data['avg-rating']) if pd.notna(book_data['avg-rating']) else None,
                num_ratings=int(book_data['num-ratings']) if pd.notna(book_data['num-ratings']) else None
            ))
        else:
            # Fallback: basic recommendation without extra info
            recommendations.append(BookRecommendation(
                title=book_name,
                author="Unknown",
                image_url=None,
                avg_rating=None,
                num_ratings=None
            ))
    
    return recommendations

# ============= API ENDPOINTS (Routes) =============
"""
Endpoints are URLs that the React app can call
Each endpoint does a specific job
"""

@app.get("/")
async def root():
    """
    Root endpoint - just to check if API is running
    
    Usage: Open http://localhost:8000 in browser
    Returns: Simple welcome message
    """
    return {
        "message": "Movie & Book Recommender API",
        "version": "2.0.0",
        "endpoints": {
            "movies": {
                "list": "/api/movies",
                "recommend": "/api/recommend"
            },
            "books": {
                "list": "/api/books",
                "popular": "/api/books/popular",
                "recommend": "/api/books/recommend"
            }
        },
        "docs": "Visit /docs for interactive API documentation"
    }

@app.get("/api/movies", response_model=MoviesResponse)
async def get_all_movies():
    """
    Get list of all available movies
    
    HTTP Method: GET (retrieving data)
    URL: http://localhost:8000/api/movies
    
    Usage in React:
        axios.get('http://localhost:8000/api/movies')
    
    Returns:
        JSON with all movie titles
    """
    try:
        # Convert dataframe column to Python list
        movie_list = movies_df['title'].tolist()
        
        return MoviesResponse(
            success=True,
            count=len(movie_list),
            movies=movie_list
        )
    except Exception as e:
        # If something goes wrong, raise HTTP error
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommend", response_model=RecommendationResponse)
async def recommend_movies(request: RecommendationRequest):
    """
    Get movie recommendations
    
    HTTP Method: POST (sending data to get result)
    URL: http://localhost:8000/api/recommend
    
    Request Body (JSON):
        {"movie": "Avatar"}
    
    Usage in React:
        axios.post('http://localhost:8000/api/recommend', {movie: "Avatar"})
    
    Returns:
        JSON with recommended movies
    """
    try:
        movie_title = request.movie
        count = request.count
        
        # Validate count range
        if count < 1:
            raise HTTPException(status_code=400, detail="Count must be at least 1")
        if count > 20:
            raise HTTPException(status_code=400, detail="Count cannot exceed 20")
        
        # Validate movie exists
        if movie_title not in movies_df['title'].values:
            raise HTTPException(
                status_code=404,
                detail=f"Movie '{movie_title}' not found in database"
            )
        
        # Get recommendations with custom count
        recommendations = get_recommendations(movie_title, top_n=count)
        
        return RecommendationResponse(
            success=True,
            movie=movie_title,
            recommendations=recommendations
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=str(e))

# ============= BOOK ENDPOINTS =============

@app.get("/api/books", response_model=BooksResponse)
async def get_all_books():
    """
    Get list of all available books for collaborative filtering
    
    HTTP Method: GET
    URL: http://localhost:8000/api/books
    
    Returns:
        JSON with all book titles available for recommendations
    """
    try:
        book_list = book_pivot.index.tolist()
        
        return BooksResponse(
            success=True,
            count=len(book_list),
            books=book_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/books/popular", response_model=PopularBooksResponse)
async def get_popular_books():
    """
    Get list of top 100 popular books
    
    HTTP Method: GET
    URL: http://localhost:8000/api/books/popular
    
    Returns:
        JSON with popular books including ratings and metadata
    """
    try:
        books_list = []
        for _, row in popular_books.iterrows():
            books_list.append(BookRecommendation(
                title=row['Book-Title'],
                author=row['Book-Author'],
                image_url=row['Image-URL-M'],
                avg_rating=float(row['avg-rating']) if pd.notna(row['avg-rating']) else None,
                num_ratings=int(row['num-ratings']) if pd.notna(row['num-ratings']) else None
            ))
        
        return PopularBooksResponse(
            success=True,
            count=len(books_list),
            books=books_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/books/recommend", response_model=BookRecommendationResponse)
async def recommend_books(request: BookRecommendationRequest):
    """
    Get book recommendations based on collaborative filtering
    
    HTTP Method: POST
    URL: http://localhost:8000/api/books/recommend
    
    Request Body (JSON):
        {"book": "1984", "count": 5}
    
    Returns:
        JSON with recommended books
    """
    try:
        book_title = request.book
        count = request.count
        
        # Validate count range
        if count < 1:
            raise HTTPException(status_code=400, detail="Count must be at least 1")
        if count > 20:
            raise HTTPException(status_code=400, detail="Count cannot exceed 20")
        
        # Validate book exists
        if book_title not in book_pivot.index:
            raise HTTPException(
                status_code=404,
                detail=f"Book '{book_title}' not found in database"
            )
        
        # Get recommendations
        recommendations = get_book_recommendations(book_title, top_n=count)
        
        return BookRecommendationResponse(
            success=True,
            book=book_title,
            recommendations=recommendations
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=str(e))

# ============= STARTUP EVENT =============
@app.on_event("startup")
async def startup_event():
    """
    Runs when the API starts
    Good place for initialization tasks
    """
    print("=" * 50)
    print("🎬📚 Movie & Book Recommender API Started!")
    print("=" * 50)
    print(f"🎬 Movies: {len(movies_df)}")
    print(f"📚 Books (Collaborative): {len(book_pivot.index)}")
    print(f"📚 Popular Books: {len(popular_books)}")
    print("=" * 50)
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🚀 API Root: http://localhost:8000")
    print("=" * 50)

# ============= RUN THE SERVER =============
"""
To run this file:
    uvicorn main:app --reload

Explanation:
- uvicorn: The server that runs FastAPI
- main: The filename (main.py)
- app: The FastAPI instance in this file
- --reload: Auto-restart when code changes
"""
