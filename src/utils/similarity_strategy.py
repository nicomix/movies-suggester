from abc import ABC, abstractmethod

from src.models.movie import Movie


class SimilarityStrategy(ABC):
    @abstractmethod
    def calculate_similarity(self, movie1: Movie, movie2: Movie) -> float:
        pass