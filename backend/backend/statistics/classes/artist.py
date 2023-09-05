
class Artist:
    def __init__(self, artist_name:str, popularity:int=None, genres:list[str]=None) -> None:
        self.artist_name = artist_name
        self.artist_popularity = popularity
        self.genres = genres

    def set_artist_popularity(self, popularity:int):
        self.artist_popularity = popularity

    def set_genres(self, genres:list[str]):
        self.genres = genres