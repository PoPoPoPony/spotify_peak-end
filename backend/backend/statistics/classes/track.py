from backend.statistics.classes.artist import Artist


class Track:
    def __init__(
            self,
            track_name:str,
            artist:Artist,
            popularity:int=None,
            acousticness:float=None,
            danceability:float=None,
            energy:float=None,
            instrumentalness:float=None,
            key:int=None,
            liveness:float=None,
            loudness:float=None,
            mode:int=None,
            speechiness:float=None,
            tempo:float=None,
            timeSignature:int=None,
            valence:float=None,
        ) -> None:
        
        self.track_name=track_name
        self.artist=artist
        self.track_popularity=popularity
        self.acousticness=acousticness
        self.danceability=danceability
        self.energy=energy
        self.instrumentalness=instrumentalness
        self.key=key
        self.liveness=liveness
        self.loudness=loudness
        self.mode=mode
        self.speechiness=speechiness
        self.tempo=tempo
        self.timeSignature=timeSignature
        self.valence=valence


    def set_track_popularity(self, popularity):
        self.track_popularity=popularity

    def set_physical_parameters(
            self,
            acousticness,
            danceability,
            energy,
            instrumentalness,
            key,
            liveness,
            loudness,
            mode,
            speechiness,
            tempo,
            timeSignature,
            valence
        ):
        self.acousticness=acousticness
        self.danceability=danceability
        self.energy=energy
        self.instrumentalness=instrumentalness
        self.key=key
        self.liveness=liveness
        self.loudness=loudness
        self.mode=mode
        self.speechiness=speechiness
        self.tempo=tempo
        self.timeSignature=timeSignature
        self.valence=valence





# 因為recent track還有times這個屬性(saved track沒有)，因此獨立成一個class
class RecentTrack(Track):
    def __init__(
            self,
            track_name: str,
            artist: Artist,
            popularity:int=None,
            acousticness:float=None,
            danceability:float=None,
            energy:float=None,
            instrumentalness:float=None,
            key:int=None,
            liveness:float=None,
            loudness:float=None,
            mode:int=None,
            speechiness:float=None,
            tempo:float=None,
            timeSignature:int=None,
            valence:float=None,
            times:int=None
        ) -> None:
        
        super().__init__(track_name, artist, popularity, acousticness, danceability, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, timeSignature, valence)     
        self.times=times

    def set_times(self, times):
        self.times=times