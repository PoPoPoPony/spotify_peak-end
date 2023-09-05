
# tag_name需先經過轉譯(track -> track_name, artist -> artist_name, genre不變)
class Tag:
    def __init__(self, tag_name:str, tag_type:str=None, tag_freq:int=None, tag_order:int=None, is_select:bool=None) -> None:
        self.tag_name=tag_name
        self.tag_type=tag_type
        self.tag_freq=tag_freq
        self.tag_order=tag_order
        self.is_select=is_select


    # set-related function will define later
