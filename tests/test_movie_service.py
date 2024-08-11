import pytest
from src.services.movie_service import MovieService
from src.models.movie import Movie
from src.utils.genre_strategy import GenreBasedSimilarityStrategy

@pytest.fixture
def sample_movies():
    return [
        Movie(
            title="Movie A",
            year=2000,
            genres=["Action"],
            ratings=[5, 4],
            viewer_count=1000,
            duration=120,
            actors=["Actor 1"],
            storyline="An action-packed adventure.",
            release_date="2000-01-01",
            content_rating="PG-13",
            poster_image="https://dummyimage.com/250x400?text=Movie+A"
        ),
        Movie(
            title="Movie B",
            year=2005,
            genres=["Drama"],
            ratings=[3, 4, 2],
            viewer_count=500,
            duration=90,
            actors=["Actor 2"],
            storyline="A dramatic story.",
            release_date="2005-05-15",
            content_rating="R",
            poster_image="https://dummyimage.com/250x400?text=Movie+B"
        ),
        Movie(
            title="Movie C",
            year=2010,
            genres=["Action", "Drama"],
            ratings=[4, 5],
            viewer_count=1500,
            duration=150,
            actors=["Actor 1", "Actor 2"],
            storyline="A thrilling action drama.",
            release_date="2010-08-20",
            content_rating="PG-13",
            poster_image="https://dummyimage.com/250x400?text=Movie+C"
        ),
    ]

def test_rank_movies_by_popularity(sample_movies):
    movie_service = MovieService(movies=sample_movies, similarity_strategy=GenreBasedSimilarityStrategy())
    ranked_movies = movie_service.rank_movies_by_popularity(top_to_down=True)

    assert ranked_movies[0].title == "Movie C"
    assert ranked_movies[1].title == "Movie A"

def test_rank_movies_by_duration(sample_movies):
    movie_service = MovieService(movies=sample_movies, similarity_strategy=GenreBasedSimilarityStrategy())
    ranked_movies = movie_service.rank_movies_by_duration(top_to_down=True)

    assert ranked_movies[0].title == "Movie C"
    assert ranked_movies[-1].title == "Movie B"

def test_find_movies_by_actor(sample_movies):
    movie_service = MovieService(movies=sample_movies, similarity_strategy=GenreBasedSimilarityStrategy())
    actor_movies = movie_service.find_movies_by_actor("Actor 1")

    assert len(actor_movies) == 2
    assert "Movie A" in [movie.title for movie in actor_movies]

def test_find_similar_movies(sample_movies):
    movie_service = MovieService(movies=sample_movies, similarity_strategy=GenreBasedSimilarityStrategy())
    similar_movies = movie_service.find_similar_movies("Movie A")

    assert len(similar_movies) > 0
