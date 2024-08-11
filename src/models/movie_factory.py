from typing import Dict
import isodate
from src.models.movie import Movie

class MovieFactory:
    @staticmethod
    def create_movie(data: Dict) -> Movie:
        duration_in_minutes = isodate.parse_duration(data['duration']).total_seconds() // 60

        return Movie(
            title=data['title'],
            year=int(data['year']),
            genres=data['genres'],
            ratings=data['ratings'],
            viewer_count=int(data['viewerCount']),
            storyline=data['storyline'],
            actors=data['actors'],
            duration=int(duration_in_minutes),
            release_date=data['releaseDate'],
            content_rating=data['contentRating'],
            poster_image=data['posterImage']
        )