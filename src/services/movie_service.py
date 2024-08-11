from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Dict, Union

from src.models.movie import Movie
from src.utils.genre_strategy import SimilarityStrategy

class MovieService:
    def __init__(self, movies: List[Movie], similarity_strategy: SimilarityStrategy):
        self.movies = movies
        self.similarity_strategy = similarity_strategy
        self.similarity_cache = self._precompute_similarities()

    def _precompute_similarities(self) -> Dict[Tuple[int, int], float]:
        similarity_cache = {}
        with ThreadPoolExecutor() as executor:
            futures = []
            for i, movie1 in enumerate(self.movies):
                for j, movie2 in enumerate(self.movies):
                    if i < j:
                        futures.append((i, j, executor.submit(self.similarity_strategy.calculate_similarity, movie1, movie2)))

            for i, j, future in futures:
                similarity_cache[(i, j)] = future.result()
                similarity_cache[(j, i)] = similarity_cache[(i, j)]

        return similarity_cache

    def _calculate_popularity(self, movie: Movie) -> float:
        rating_weight = 0.7
        total_ratings_weight = 0.2
        viewer_count_weight = 0.1

        average_rating = movie.imdb_rating
        total_ratings = len(movie.ratings)
        viewer_count = movie.viewer_count

        normalized_viewer_count = viewer_count / 1_000_000

        popularity_score = (
            (average_rating * rating_weight) +
            (total_ratings * total_ratings_weight) +
            (normalized_viewer_count * viewer_count_weight)
        )

        return popularity_score

    def rank_movies_by_popularity(self, top_to_down: bool = True, top_n: int = 10) -> List[Movie]:
        """
        Ranks movies by their popularity.

        Parameters:
        - top_to_down (bool): Determines the order of sorting. True for descending, False for ascending.
        - top_n (int): The number of top movies to return.

        Returns:
        List[Movie]: A list of movies sorted by popularity, limited to the top_n results.
        """
        sorted_movies = sorted(
            self.movies,
            key=self._calculate_popularity,
            reverse=top_to_down
        )
        return sorted_movies[:top_n]

    def find_similar_movies(self, target_movie: str, top_n: int = 10) -> List[Dict[str, Union[Movie, float]]]:
        """
        Finds movies similar to a given movie.

        Parameters:
        - target_movie (Movie): The movie to find similarities to.
        - top_n (int): The number of similar movies to return.

        Returns:
        List[Tuple[Movie, float]]: A list of tuples containing the similar movies and their similarity scores, limited to the top_n results.
        """
        target_movie_object = next((movie for movie in self.movies if movie.title == target_movie), None)
        if target_movie_object is None:
            raise ValueError("Movie with the given title not found.")

        target_index = self.movies.index(target_movie_object)
        similarities = [
            {"movie": self.movies[i], "similarity_score": self.similarity_cache[(target_index, i)]}
            for i in range(len(self.movies)) if i != target_index
        ]
        similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similarities[:top_n]

    def find_movies_by_actor(self, actor: str) -> List[Movie]:
        """
        Finds all movies featuring a specific actor.

        Parameters:
        - actor (str): The name of the actor to filter movies by.

        Returns:
        List[Movie]: A list of movies that feature the specified actor.
        """
        return [movie for movie in self.movies if actor in movie.actors]

    def rank_movies_by_duration(self, top_to_down: bool = True, top_n: int = 10) -> List[Movie]:
        """
        Ranks movies by their duration.

        Parameters:
        - top_to_down (bool): Determines the order of sorting. True for descending, False for ascending.
        - top_n (int): The number of top movies to return based on duration.

        Returns:
        List[Movie]: A list of movies sorted by duration, limited to the top_n results.
        """
        return sorted(self.movies, key=lambda movie: movie.duration, reverse=top_to_down)[:top_n]

    def rank_movies_by_year(self, top_to_down: bool = True, top_n: int = 10) -> List[Movie]:
        """
        Ranks movies by their release year.

        Parameters:
        - top_to_down (bool): Determines the order of sorting. True for descending, False for ascending.
        - top_n (int): The number of top movies to return based on release year.

        Returns:
        List[Movie]: A list of movies sorted by release year, limited to the top_n results.
        """
        return sorted(self.movies, key=lambda movie: int(movie.year), reverse=top_to_down)[:top_n]

