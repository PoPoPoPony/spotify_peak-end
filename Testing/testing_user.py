from random import randint
from random import shuffle
from random import choices
import backend_utils
import glob
import os
import json


class User:
    def __init__(self, args):
        if 'email' not in args: # if not given email then init one
            user_len = len(backend_utils.get_users("*"))
            email = f'selenium_test{user_len}@gmail.com'
        else :
            email = args.email
        self.email = email
        self.user_name = args.user_name


    def set_song_lst_id(self, id, list_type):
        if list_type == 'WD':
            self.WD_ID = id
        elif list_type == 'T':
            self.T_ID = id

    def set_user_id(self, id):
        self.user_id = id



class FirstStageTestingUser(User):
    def __init__(self, args):
        user_jsons = [os.path.split(x)[-1] for x in glob.glob("users_json/first/*.json")]
        self.physical_user_name = args.physical_user_name
        if f"{args.user_name}.json" in user_jsons:
            with open(f"users_json/first/{args.user_name}.json", 'r', encoding='utf8') as f:
                data = json.load(f)

            args.email = data['email']
            super().__init__(args)

            self.first_stage_group = data['first_stage_group']
            self.is_add = data['is_add']
            self.UI = data['UI']
            self.list_type = data['list_type']
            self.weekly_like_scores = data['weekly_like_scores']
            self.weekly_splendid_scores = data['weekly_splendid_scores']
            self.weekly_listened = data['weekly_listened']
            self.weekly_song_lst_added = data['weekly_song_lst_added']
            self.weekly_satisfy = data['weekly_satisfy']
            self.weekly_novelty = data['weekly_novelty']
            self.weekly_diversity = data['weekly_diversity']
            self.tag_like_scores = data['tag_like_scores']
            self.tag_splendid_scores = data['tag_splendid_scores']
            self.tag_listened = data['tag_listened']
            self.tag_song_lst_added = data['tag_song_lst_added']
            self.tag_satisfy = data['tag_satisfy']
            self.tag_novelty = data['tag_novelty']
            self.tag_diversity = data['tag_diversity']
            self.tags = data['tags']

        else:
            super().__init__(args)
            self.first_stage_group = args.first_stage_group
            

            if args.first_stage_group>4:
                self.is_add = True
            else:
                self.is_add = False

            if args.first_stage_group in [1, 3, 5, 7]:
                self.UI = ['list', 'single']
            else:
                self.UI = ['single', 'list']

            if args.first_stage_group in [1, 2, 5, 6]:
                self.list_type = ["WD", "T"]
            else:
                self.list_type = ["T", "WD"]

            # weekly-related scores
            self.weekly_like_scores = [randint(1, 10) for _ in range(20)]
            self.weekly_splendid_scores = [randint(1, 10) for _ in range(20)]

            idxs = list(range(20))
            shuffle(idxs)

            self.weekly_listened = idxs[:5]

            shuffle(idxs)
            if self.is_add:
                self.weekly_song_lst_added = idxs[:5]
            else:
                self.weekly_song_lst_added = []
            self.weekly_satisfy = randint(1, 10)
            self.weekly_novelty = randint(1, 10)
            self.weekly_diversity = randint(1, 10)

            # tag-related scores
            self.tag_like_scores = [randint(1, 10) for _ in range(20)]
            self.tag_splendid_scores = [randint(1, 10) for _ in range(20)]

            shuffle(idxs)
            self.tag_listened = idxs[:5]

            shuffle(idxs)
            if self.is_add:
                self.tag_song_lst_added = idxs[:5]
            else:
                self.tag_song_lst_added = []
            self.tag_satisfy = randint(1, 10)
            self.tag_novelty = randint(1, 10)
            self.tag_diversity = randint(1, 10)

            self.tags = choices(range(10), k=3)


class SecondStageTestingUser(User):
    def __init__(self, args):
        self.email = args.email
        self.user_name = args.user_name
        user_info = backend_utils.get_users(self.email)
        self.secondaryType = user_info['secondaryType']
        
        super().set_user_id(user_info['userID'])

        first_stage_WD_ID = backend_utils.get_song_lst_id(self.user_id, "Weekly_Discovery", "first")['songListID']
        super().set_song_lst_id(first_stage_WD_ID, "WD")

        first_stage_T_ID = backend_utils.get_song_lst_id(self.user_id, "Tags", "first")['songListID']
        super().set_song_lst_id(first_stage_T_ID, "T")

        # secondary type
        # 0: week(高->低) -> tag(低->高)
        # 1: week(低->高) -> tag(高->低)
        # 2: tag(高->低) -> week(低->高)
        # 3: tag(低->高) -> week(高->低)

        # set up songs order from DB


        if self.secondaryType == 0:
            self.list_type = ['WD', 'T']
            WD_elems = backend_utils.get_song_lst_elem(self.WD_ID, rule_type='like', order=1)
            T_elems = backend_utils.get_song_lst_elem(self.T_ID, rule_type='like', order=0)
        elif self.secondaryType == 1:
            self.list_type = ['WD', 'T']
            WD_elems = backend_utils.get_song_lst_elem(self.WD_ID, rule_type='like', order=0)
            T_elems = backend_utils.get_song_lst_elem(self.T_ID, rule_type='like', order=1)
        elif self.secondaryType == 2:
            self.list_type = ['T', 'WD']
            WD_elems = backend_utils.get_song_lst_elem(self.WD_ID, rule_type='like', order=0)
            T_elems = backend_utils.get_song_lst_elem(self.T_ID, rule_type='like', order=1)
        elif self.secondaryType == 3:
            self.list_type = ['T', 'WD']
            WD_elems = backend_utils.get_song_lst_elem(self.WD_ID, rule_type='like', order=1)
            T_elems = backend_utils.get_song_lst_elem(self.T_ID, rule_type='like', order=0)

        self.DB_WD_names = [backend_utils.get_song_name_by_ID(x['trackID'])['trackName'] for x in WD_elems]
        self.DB_WD_likes = [x['likeScore'] for x in WD_elems]
        self.DB_T_names = [backend_utils.get_song_name_by_ID(x['trackID'])['trackName'] for x in T_elems]
        self.DB_T_likes = [x['likeScore'] for x in T_elems]


        self.weekly_satisfy = randint(1, 10)
        self.weekly_novelty = randint(1, 10)
        self.weekly_diversity = randint(1, 10)

        self.tag_satisfy = randint(1, 10)
        self.tag_novelty = randint(1, 10)
        self.tag_diversity = randint(1, 10)
