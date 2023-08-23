from testing_user import FirstStageTestingUser, SecondStageTestingUser
import backend_utils
from typing import Union

def compare(IN, DB, title:str):
    print(title)
    print(f"Input: {IN}")
    print(f"DB:    {DB}")

    print("="*30)

# def translate(obj):
#     if isinstance(obj, str):
#         return obj
#     elif isinstance(obj, list)

def check_group(testing_user: FirstStageTestingUser):
    IN = testing_user.first_stage_group
    DB = backend_utils.get_users(testing_user.email)

    compare(IN, DB, "Testing group")


def check_song_lst_elem(testing_user: FirstStageTestingUser):
    DB_elems = backend_utils.get_song_lst_elems(testing_user.WD_ID, rule_type='order', order=0)
    
    # WD like score
    DB_like_scores = [x['likeScore'] for x in DB_elems]
    IN_like_scores = testing_user.weekly_like_scores

    compare(IN_like_scores, DB_like_scores, "WD like score")

    # WD splendid score
    DB_splendid_scores = [x['splendidScore'] for x in DB_elems]
    IN_splendid_scores = testing_user.weekly_splendid_scores

    compare(IN_splendid_scores, DB_splendid_scores, "WD splendid score")

    # WD listened
    DB_listened = [i for i in range(len(DB_elems)) if DB_elems[i]['beforeListened']]
    IN_listened = sorted(testing_user.weekly_listened)

    compare(IN_listened, DB_listened, "WD listened")

    # WD added
    DB_added = [i for i in range(len(DB_elems)) if DB_elems[i]['addSongList']]
    IN_added = sorted(testing_user.weekly_song_lst_added)

    compare(IN_added, DB_added, "WD added")


    DB_elems = backend_utils.get_song_lst_elems(testing_user.T_ID, rule_type='order', order=0)
    
    # WD like score
    DB_like_scores = [x['likeScore'] for x in DB_elems]
    IN_like_scores = testing_user.tag_like_scores

    compare(IN_like_scores, DB_like_scores, "T like score")

    # WD splendid score
    DB_splendid_scores = [x['splendidScore'] for x in DB_elems]
    IN_splendid_scores = testing_user.tag_splendid_scores

    compare(IN_splendid_scores, DB_splendid_scores, "T splendid score")

    # WD listened
    DB_listened = [i for i in range(len(DB_elems)) if DB_elems[i]['beforeListened']]
    IN_listened = sorted(testing_user.tag_listened)

    compare(IN_listened, DB_listened, "T listened")

    # WD added
    DB_added = [i for i in range(len(DB_elems)) if DB_elems[i]['addSongList']]
    IN_added = sorted(testing_user.tag_song_lst_added)

    compare(IN_added, DB_added, "T added")


def check_song_lst_score(testing_user: Union[FirstStageTestingUser, SecondStageTestingUser]):
    DB = backend_utils.get_song_lst_score(testing_user.WD_ID)
    IN = {
        'satisfyScore': testing_user.weekly_satisfy,
        'diversityScore': testing_user.weekly_diversity,
        'noveltyScore ': testing_user.weekly_novelty
    }

    compare(IN, DB, "WD song list score")

    DB = backend_utils.get_song_lst_score(testing_user.T_ID)
    IN = {
        'satisfyScore': testing_user.tag_satisfy,
        'diversityScore': testing_user.tag_diversity,
        'noveltyScore ': testing_user.tag_novelty
    }

    compare(IN, DB, "T song list score")


def check_tags(testing_user: FirstStageTestingUser):
    DB_tag_genre = backend_utils.get_tags(testing_user.user_id, tag_type="genre")
    DB_tag_artist = backend_utils.get_tags(testing_user.user_id, tag_type="artist")
    DB_tag_track = backend_utils.get_tags(testing_user.user_id, tag_type="track")
    

    # check length of tag
    print(f"length of the genre tags: {len(DB_tag_genre)}")
    print(f"length of the artist tags: {len(DB_tag_artist)}")
    print(f"length of the track tags: {len(DB_tag_track)}")

    print("="*30)

    DB_tag_genre_selected = [x['order'] for x in DB_tag_genre if x['tagSelected']]
    # same as the order in the website
    IN_tag_genre_selected = [testing_user.tags[0]]

    compare(IN_tag_genre_selected, DB_tag_genre_selected, "Tag genre selected")

    DB_tag_artist_selected = [x['order'] for x in DB_tag_artist if x['tagSelected']]
    # same as the order in the website
    IN_tag_artist_selected = [testing_user.tags[1]]

    compare(IN_tag_artist_selected, DB_tag_artist_selected, "Tag artist selected")

    DB_tag_track_selected = [x['order'] for x in DB_tag_track if x['tagSelected']]
    # same as the order in the website
    IN_tag_track_selected = [testing_user.tags[2]]

    compare(IN_tag_track_selected, DB_tag_track_selected, "Tag track selected")

def check_song_lst_name_order(testing_user: SecondStageTestingUser):
    compare(testing_user.IN_WD_names, testing_user.DB_WD_names, "WD song names")
    compare(testing_user.IN_T_names, testing_user.DB_T_names, "T song names")