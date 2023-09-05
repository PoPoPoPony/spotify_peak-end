class AudioFeatures:
    def __init__(
            self,
            min_acousticness:float=None,
            target_acousticness:float=None,
            max_acousticness:float=None,
            min_danceability:float=None,
            target_danceability:float=None,
            max_danceability:float=None,
            min_energy:float=None,
            target_energy:float=None,
            max_energy:float=None,
            min_instrumentalness:float=None,
            target_instrumentalness:float=None,
            max_instrumentalness:float=None,
            min_key:int=None,
            target_key:int=None,
            max_key:int=None,
            min_liveness:float=None,
            target_liveness:float=None,
            max_liveness:float=None,
            min_tempo:float=None,
            target_tempo:float=None,
            max_tempo:float=None,
            min_valence:float=None,
            target_valence:float=None,
            max_valence:float=None,
        ) -> None:
            self.min_acousticness=min_acousticness
            self.target_acousticness=target_acousticness
            self.max_acousticness=max_acousticness
            self.min_danceability=min_danceability
            self.target_danceability=target_danceability
            self.max_danceability=max_danceability
            self.min_energy=min_energy
            self.target_energy=target_energy
            self.max_energy=max_energy
            self.min_instrumentalness=min_instrumentalness
            self.target_instrumentalness=target_instrumentalness
            self.max_instrumentalness=max_instrumentalness
            self.min_key=min_key
            self.target_key=target_key
            self.max_key=max_key
            self.min_liveness=min_liveness
            self.target_liveness=target_liveness
            self.max_liveness=max_liveness
            self.min_tempo=min_tempo
            self.target_tempo=target_tempo
            self.max_tempo=max_tempo
            self.min_valence=min_valence
            self.target_valence=target_valence
            self.max_valence=max_valence

    # set-related function will define later