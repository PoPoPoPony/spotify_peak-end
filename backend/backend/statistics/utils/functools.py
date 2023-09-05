import backend.statistics.utils.backend as backend
from backend.statistics.classes.artist import Artist
from backend.statistics.classes.audio_features import AudioFeatures
from backend.statistics.classes.songlist import SongList, SongListElem
from backend.statistics.classes.tag import Tag
from backend.statistics.classes.track import Track, RecentTrack
from backend.statistics.classes.user import User

# get track infos and artist infos
def get_basic_infos(track_ids: list[str]):
    track_infos = backend.get_track_infos(track_ids=track_ids)
    songlist_artist_ids = [track_info['artistID'] for track_info in track_infos]
    artist_infos = backend.get_artist_infos(artist_ids=songlist_artist_ids)

    return track_infos, artist_infos


def expand_all_attribute(instance):
    d = {}
    for key, val in instance.__dict__.items():
        if isinstance(val, (Artist, AudioFeatures, SongList, SongListElem, Tag, Track, RecentTrack, User)):
            for k, v in expand_all_attribute(val).items():
                d[k] = v
        else:
            d[key] = val
    return d