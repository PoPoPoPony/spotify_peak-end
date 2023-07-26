import argparse


def get_first_stage_user_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first_stage_group", default=1, type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8])
    parser.add_argument("--user_name", default="test_0718_1", type=str)
    parser.add_argument("--physical_user_name", default="pony", type=str)

    return parser.parse_args()


def get_second_stage_user_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", type=str)
    parser.add_argument("--user_name", default="test_0718_1", type=str)

    return parser.parse_args()