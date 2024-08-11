import json
from fastapi import APIRouter, HTTPException
from typing import Dict, List, Union
from src.models.movie import Movie
from src.models.movie_factory import MovieFactory
from src.services.movie_service import MovieService
from src.utils.genre_strategy import GenreBasedSimilarityStrategy

router = APIRouter()

with open("src/movies.json", "r") as file:
    database = json.load(file)

movies = [MovieFactory.create_movie(movie) for movie in database]

similarity_strategy = GenreBasedSimilarityStrategy()
movie_service = MovieService(movies, similarity_strategy)

@router.get("/movies/popularity", response_model=List[Movie])
def get_movies_by_popularity(top_to_down: bool = True, top_n: int = 10):
    """
    Get movies sorted by popularity.

    Parameters:
    - top_to_down: bool = True (Optional, default is True) - If True, returns movies from most to least popular.
    - top_n: int = 10 (Optional, default is 10) - The number of top movies to return.


    Returns:
    - List[Movie]: A list of movies sorted by popularity.
    """
    return movie_service.rank_movies_by_popularity(top_to_down, top_n)

@router.get("/movies/similar", response_model=List[Dict[str, Union[Movie, float]]])
def get_similar_movies(title: str, top_n: int = 10):
    """
    Get movies similar to a given title.

    Parameters:
    - title: str - The title of the movie to find similar movies for.
    - top_n: int = 10 (Optional, default is 10) - The number of top movies to return.

    Returns:
    - List[Movie]: A list of similar movies.

    Raises:
    - HTTPException: 404 error if no similar movies are found.
    """
    similar_movies = movie_service.find_similar_movies(title, top_n)
    if not similar_movies:
        raise HTTPException(status_code=404, detail="Movie not found or no similar movies")
    return similar_movies

@router.get("/movies/actor", response_model=List[Movie])
def get_movies_by_actor(actor_name: str, top_n: int = 10):
    """
    Get movies featuring a specific actor.

    Parameters:
    - actor_name: str - The name of the actor to find movies for.
    - top_n: int = 10 (Optional, default is 10) - The number of top movies to return.

    Returns:
    - List[Movie]: A list of movies featuring the specified actor.

    Raises:
    - HTTPException: 404 error if no movies are found with the specified actor.
    """
    movies_with_actor = movie_service.find_movies_by_actor(actor_name, top_n)
    if not movies_with_actor:
        raise HTTPException(status_code=404, detail="No movies found featuring this actor")
    return movies_with_actor

@router.get("/movies/duration", response_model=List[Movie])
def get_movies_by_duration(top_to_down: bool = True, top_n: int = 10):
    """
    Get movies sorted by duration.

    Parameters:
    - top_to_down: bool = True (Optional, default is True) - If True, returns movies from longest to shortest.
    - top_n: int = 10 (Optional, default is 10) - The number of top movies to return.

    Returns:
    - List[Movie]: A list of movies sorted by duration.
    """
    return movie_service.rank_movies_by_duration(top_to_down, top_n)

@router.get("/movies/year", response_model=List[Movie])
def get_movies_by_year(top_to_down: bool = True, top_n: int = 10):
    """
    Get movies sorted by release year.

    Parameters:
    - top_to_down: bool = True (Optional, default is True) - If True, returns movies from most recent to oldest.
    - top_n: int = 10 (Optional, default is 10) - The number of top movies to return.

    Returns:
    - List[Movie]: A list of movies sorted by release year.
    """
    return movie_service.rank_movies_by_year(top_to_down, top_n)