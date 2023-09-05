from backend.statistics.classes.user import User
from backend.statistics.classes.songlist import SongList, SongListElem
from backend.statistics.classes.track import Track, RecentTrack
from backend.statistics.classes.artist import Artist
from backend.statistics.classes.tag import Tag
from backend.statistics.classes.audio_features import AudioFeatures
import backend.statistics.utils.backend as backend
import backend.statistics.utils.functools as functools
import pandas as pd





def initialize_users(user_emails: list[str]):
    users = []
    
    # initializing user
    user_infos = backend.get_users(user_emails)
    for user_info in user_infos:
        users.append(User(
            user_email=user_info['userEmail'],
            user_id=user_info['userID'],
            between_type=user_info['betweenType'],
            within_type=user_info['withinType'],
            secondary_type=user_info['secondaryType']
        ))


    for user in users:
        # processing sonlist-related data
        songlist_infos = backend.get_songlist_info(user.user_id, list_type='*', period='*')
        songlists = []
        for songlist_info in songlist_infos:
            songlist = SongList(songlist_id=songlist_info['songListID'], list_type=songlist_info['listType'], period=songlist_info['period'])
            songlist_score = backend.get_songlist_score(songlist_id=songlist.songlist_id)
            songlist.set_satisfy_score(songlist_score['satisfyScore'])
            songlist.set_diversity_score(songlist_score['diversityScore'])
            songlist.set_novelty_score(songlist_score['noveltyScore'])

            # rule_type為指定一個欄位排序, order(0:遞增，1:遞減, 其他:不排序)
            songlist_elems = backend.get_songlist_elems(songlist_id=songlist.songlist_id, rule_type='order', order=-1)
            songlist_track_ids = [songlist_elem['trackID'] for songlist_elem in songlist_elems]
            track_infos, artist_infos = functools.get_basic_infos(songlist_track_ids)

            elems = []
            for i in range(len(songlist_elems)):
                elem = SongListElem(
                    track=Track(
                        track_name=track_infos[i]['trackName'],
                        artist=Artist(
                            artist_name=artist_infos[i]['artistName'],
                            popularity=artist_infos[i]['popularity'],
                            genres=artist_infos[i]['genres']
                        ),
                        popularity=track_infos[i]['popularity'],
                        acousticness=track_infos[i]['acousticness'],
                        danceability=track_infos[i]['danceability'],
                        energy=track_infos[i]['energy'],
                        instrumentalness=track_infos[i]['instrumentalness'],
                        key=track_infos[i]['key'],
                        liveness=track_infos[i]['liveness'],
                        loudness=track_infos[i]['loudness'],
                        mode=track_infos[i]['mode'],
                        speechiness=track_infos[i]['speechiness'],
                        tempo=track_infos[i]['tempo'],
                        timeSignature=track_infos[i]['timeSignature'],
                        valence=track_infos[i]['valence']
                    ),
                    like_score=songlist_elems[i]['likeScore'],
                    splendid_score=songlist_elems[i]['splendidScore'],
                    is_add=songlist_elems[i]['addSongList'],
                    songlist_elem_order=songlist_elems[i]['order'],
                    is_before_listened=songlist_elems[i]['beforeListened'],
                    recommend=songlist_elems[i]['recommend']
                )
                elems.append(elem)
            songlist.set_songlist_elems(elems)
            songlists.append(songlist)
        user.set_song_lists(songlists)

        # processing user saved Track
        user_saved_track_infos = backend.get_saved_track_infos(user_id=user.user_id)
        if user_saved_track_infos:
            user_saved_track_ids = [elem['trackID'] for elem in user_saved_track_infos]
            track_infos, artist_infos = functools.get_basic_infos(user_saved_track_ids)
            tracks=[]
            for i in range(len(track_infos)):
                tracks.append(Track(
                    track_name=track_infos[i]['trackName'],
                    artist=Artist(
                        artist_name=artist_infos[i]['artistName'],
                        popularity=artist_infos[i]['popularity'],
                        genres=artist_infos[i]['genres']
                    ),
                    popularity=track_infos[i]['popularity'],
                    acousticness=track_infos[i]['acousticness'],
                    danceability=track_infos[i]['danceability'],
                    energy=track_infos[i]['energy'],
                    instrumentalness=track_infos[i]['instrumentalness'],
                    key=track_infos[i]['key'],
                    liveness=track_infos[i]['liveness'],
                    loudness=track_infos[i]['loudness'],
                    mode=track_infos[i]['mode'],
                    speechiness=track_infos[i]['speechiness'],
                    tempo=track_infos[i]['tempo'],
                    timeSignature=track_infos[i]['timeSignature'],
                    valence=track_infos[i]['valence']
                ))
            user.set_user_saved_tracks(tracks)
        else:
            user.set_user_saved_tracks([])

        # processing user recent Track
        recent_track_infos = backend.get_recent_track_infos(user_id=user.user_id)
        user_recent_track_ids = [elem['trackID'] for elem in recent_track_infos]
        track_infos, artist_infos = functools.get_basic_infos(user_recent_track_ids)
        recent_tracks=[]
        for i in range(len(track_infos)):
            recent_tracks.append(RecentTrack(
                track_name=track_infos[i]['trackName'],
                artist=Artist(
                    artist_name=artist_infos[i]['artistName'],
                    popularity=artist_infos[i]['popularity'],
                    genres=artist_infos[i]['genres']
                ),
                popularity=track_infos[i]['popularity'],
                acousticness=track_infos[i]['acousticness'],
                danceability=track_infos[i]['danceability'],
                energy=track_infos[i]['energy'],
                instrumentalness=track_infos[i]['instrumentalness'],
                key=track_infos[i]['key'],
                liveness=track_infos[i]['liveness'],
                loudness=track_infos[i]['loudness'],
                mode=track_infos[i]['mode'],
                speechiness=track_infos[i]['speechiness'],
                tempo=track_infos[i]['tempo'],
                timeSignature=track_infos[i]['timeSignature'],
                valence=track_infos[i]['valence'],
                times=recent_track_infos[i]['times']
            ))
        user.set_user_recent_tracks(recent_tracks)
        
        # processing user Tags
        tag_infos = backend.get_tag_infos(user_id=user.user_id, tag_type="*", order=-1, is_select="*")
        tags = []
        for tag_info in tag_infos:
            if tag_info['tagType']=='track':
                tag_name = backend.get_track_infos([tag_info['tagID']])[0]['trackName']
            elif tag_info['tagType']=='artist':
                tag_name = backend.get_artist_infos([tag_info['tagID']])[0]['artistName']
            else: 
                tag_name=tag_info['tagID']

            tags.append(Tag(
                tag_name=tag_name,
                tag_type=tag_info['tagType'],
                tag_freq=tag_info['tagFreq'],
                tag_order=tag_info['order'],
                is_select=tag_info['tagSelected']
            ))
        
        user.set_tags(tags)

        # processing user audio features
        user_audio_features_info = backend.get_audio_features(user_id=user.user_id)
        # rename是為了比較好建立instance，因為資料庫中的命名格式不同(DB: minKey, class: min_key)
        user_audio_features_info_rename = {}
        for key, val in user_audio_features_info.items():
            # userID 不用存
            if key != 'userID':
                new_key = key
                new_key = new_key.replace('min', 'min_')
                new_key = new_key.replace('max', 'max_')
                new_key = new_key.replace('target', 'target_')
                new_key = new_key.lower()

                user_audio_features_info_rename[new_key] = val

        audio_feature = AudioFeatures(**user_audio_features_info_rename)
        user.set_audio_features(audio_feature)
    return users




def make_saved_tracks_df(users: list[User]):
    # make the user saved tracks table
    data = []
    col_names = ["user_email", "between_type", "within_type", "secondary_type"]
    ini = True

    for user in users:
        for saved_track in user.saved_tracks:
            d = [user.user_email, user.between_type, user.within_type, user.secondary_type]
            dict_ = functools.expand_all_attribute(saved_track)
            for key, val in dict_.items():
                d.append(val)
                if ini:
                    col_names.append(key)
            ini = False
            data.append(d)
    df = pd.DataFrame(data, columns=col_names)
    return df



def make_recent_tracks_df(users: list[User]):
    # make the user recent tracks table
    data = []
    col_names = ["user_email", "between_type", "within_type", "secondary_type"]
    ini = True

    for user in users:
        for recent_track in user.recent_tracks:
            d = [user.user_email, user.between_type, user.within_type, user.secondary_type]
            dict_ = functools.expand_all_attribute(recent_track)
            for key, val in dict_.items():
                d.append(val)
                if ini:
                    col_names.append(key)
            ini = False
            data.append(d)
    df = pd.DataFrame(data, columns=col_names)
    return df

def make_tag_df(users: list[User]):
    # make the tag table
    data = []
    col_names = ["user_email", "between_type", "within_type", "secondary_type"]
    ini = True

    for user in users:
        for tag in user.tags:
            d = [user.user_email, user.between_type, user.within_type, user.secondary_type]
            dict_ = functools.expand_all_attribute(tag)
            for key, val in dict_.items():
                d.append(val)
                if ini:
                    col_names.append(key)
            ini = False
            data.append(d)
    df = pd.DataFrame(data, columns=col_names)
    return df

def make_songlist_df(users: list[User]):
    # make the songlist table
    data = []
    col_names = ["user_email", "between_type", "within_type", "secondary_type"]
    ini = True

    for user in users:
        for songlist in user.songlists:
            dict_ = functools.expand_all_attribute(songlist)
            for key, val in dict_.items():
                if isinstance(val, list):
                    for elem in val:
                        sub_dict = functools.expand_all_attribute(elem)
                        sub_dict.update(dict_)
                        sub_dict.pop(key)
                        sub_dict.pop("songlist_id")

                        d = [user.user_email, user.between_type, user.within_type, user.secondary_type]
                        for k, v in sub_dict.items():
                            d.append(v)
                            if ini :
                                col_names.append(k)
                        ini = False
                        data.append(d)
    df = pd.DataFrame(data, columns=col_names)
    return df


def make_user_audio_fetures_df(users: list[User]):
    # make the tag table
    data = []
    col_names = ["user_email", "between_type", "within_type", "secondary_type"]
    ini = True

    for user in users:
        d = [user.user_email, user.between_type, user.within_type, user.secondary_type]
        dict_ = functools.expand_all_attribute(user.audio_features)
        for key, val in dict_.items():
            d.append(val)
            if ini:
                col_names.append(key)
        ini = False
        data.append(d)
    df = pd.DataFrame(data, columns=col_names)
    return df


def main():
    # user_emails = ['mindyling.c@gmail.com', "koctober1012@gmail.com"]
    user_emails = "*"
    users = initialize_users(user_emails)

    df = make_saved_tracks_df(users)
    df.to_csv("backend/static/saved_tracks.csv", encoding="utf-8", index=False)

    df = make_recent_tracks_df(users)
    df.to_csv("backend/static/recent_tracks.csv", encoding="utf-8", index=False)

    df = make_tag_df(users)
    df.to_csv("backend/static/tags.csv", encoding="utf-8", index=False)

    df = make_songlist_df(users)
    df.to_csv("backend/static/songlist.csv", encoding="utf-8", index=False)

    df = make_user_audio_fetures_df(users)
    df.to_csv("backend/static/audio_features.csv", encoding="utf-8", index=False)













if __name__ == '__main__':
    main()