from typing import List

from src.models.movie import Movie
from src.utils.similarity_strategy import SimilarityStrategy

class GenreBasedSimilarityStrategy(SimilarityStrategy):
    def calculate_similarity(self, movie1: Movie, movie2: Movie) -> float:
        genre_weight = 0.6
        rating_weight = 0.3
        cast_weight = 0.1

        genre_similarity = self._calculate_genre_similarity(movie1.genres, movie2.genres)
        rating_similarity = self._calculate_rating_similarity(movie1.imdb_rating, movie2.imdb_rating)
        cast_similarity = self._calculate_cast_similarity(movie1.actors, movie2.actors)

        return (genre_similarity * genre_weight) + (rating_similarity * rating_weight) + (cast_similarity * cast_weight)

    def _calculate_genre_similarity(self, genres1: List[str], genres2: List[str]) -> float:
        common_genres = set(genres1).intersection(set(genres2))
        total_genres = set(genres1).union(set(genres2))
        return len(common_genres) / len(total_genres) if total_genres else 0.0

    def _calculate_rating_similarity(self, rating1: float, rating2: float) -> float:
        return 1.0 - abs(rating1 - rating2) / 10.0  # Normalize difference over 10

    def _calculate_cast_similarity(self, cast1: List[str], cast2: List[str]) -> float:
        common_cast = set(cast1).intersection(set(cast2))
        total_cast = set(cast1).union(set(cast2))
        return len(common_cast) / len(total_cast) if total_cast else 0.0
