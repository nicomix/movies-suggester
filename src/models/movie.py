from typing import List
from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    year: int
    genres: List[str]
    ratings: List[int]
    viewer_count: int
    storyline: str
    actors: List[str]
    duration: int  # Duration is stored as minutes
    release_date: str
    content_rating: str
    poster_image: str

    @property
    def imdb_rating(self) -> float:
        """Calculate the average IMDB rating."""
        return sum(self.ratings) / len(self.ratings) if self.ratings else 0.0