from backend.statistics.classes.track import Track, RecentTrack
from backend.statistics.classes.tag import Tag
from backend.statistics.classes.audio_features import AudioFeatures
from backend.statistics.classes.songlist import SongList


class User:
    def __init__(self, user_email:str, user_id:str=None, between_type:int=None, within_type:int=None, secondary_type:int=None) -> None:
        self.user_email = user_email
        self.user_id = user_id
        self.between_type = between_type
        self.within_type = within_type
        self.secondary_type = secondary_type
        self.saved_tracks = None
        self.recent_tracks = None
        self.tags = None
        self.audio_features = None
        self.songlists = None


    def set_user_saved_tracks(self, saved_tracks:list[Track]):
        self.saved_tracks=saved_tracks

    def set_user_recent_tracks(self, recent_tracks:list[RecentTrack]):
        self.recent_tracks=recent_tracks

    def set_tags(self, tags:list[Tag]):
        self.tags=tags

    def set_audio_features(self, audio_features:list[AudioFeatures]):
        self.audio_features=audio_features

    def set_song_lists(self, songlists:list[SongList]):
        self.songlists=songlists