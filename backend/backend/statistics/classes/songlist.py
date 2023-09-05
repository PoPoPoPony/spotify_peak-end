from backend.statistics.classes.track import Track


# only track is required
class SongListElem:
    def __init__(
            self,
            track:Track,
            like_score:int=None,
            splendid_score:int=None,
            is_add:bool=None,
            songlist_elem_order:int=None,
            is_before_listened:bool=None,
            recommend:str=None
        ) -> None:

        self.track = track
        self.like_score = like_score
        self.splendid_score = splendid_score
        self.is_add = is_add
        self.songlist_elem_order = songlist_elem_order
        self.is_before_listened = is_before_listened
        self.recommend = recommend

    def set_like_score(self, score):
        self.like_score = score

    def set_splendid_score(self, score):
        self.splendid_score = score

    def set_is_add(self, is_add):
        self.is_add = is_add

    def set_songlist_elem_order(self, songlist_elem_order):
        self.songlist_elem_order = songlist_elem_order

    def set_is_before_listened(self, is_before_listened):
        self.is_before_listened = is_before_listened

    def set_recommend(self, recommend):
        self.recommend = recommend
    



# only songlist_id is required
class SongList:
    def __init__(
            self,
            songlist_id:str,
            list_type:str=None,
            period:str=None,
            satisfy_score:int=None,
            diversity_score:int=None,
            novelty_score:int=None,
            songlist_elems:list[SongListElem]=None
        ) -> None:


        self.songlist_id = songlist_id
        self.list_type = list_type
        self.period = period
        self.satisfy_score = satisfy_score
        self.diversity_score = diversity_score
        self.novelty_score = novelty_score
        self.songlist_elems = songlist_elems


    def set_list_type(self, list_type:str):
        self.list_type = list_type

    def set_period(self, period:str):
        self.period = period

    def set_satisfy_score(self, score:int):
        self.satisfy_score = score

    def set_diversity_score(self, score:int):
        self.diversity_score = score

    def set_novelty_score(self, score:int):
        self.novelty_score = score

    def set_songlist_elems(self, elems:list[SongListElem]):
        self.songlist_elems = elems