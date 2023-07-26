from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from options import get_second_stage_user_options
import page
from testing_user import SecondStageTestingUser
import check
import backend_utils
import os
import json
from dotenv import dotenv_values


def main():
    physical_users = dotenv_values(".env")
    user_options = get_second_stage_user_options()
    # 根據user_name查詢第一次測驗的資料的email、account、password
    try:
        with open(f"users_json/first/{user_options.user_name}.json", 'r', encoding='utf8') as f:
            data = json.load(f)
            user_options.email = data['email']
            physical_user_name = data['physical_user_name']
    except Exception as e:
        print(f"Faild to load users_json/first/{user_options.user_name}.json")
        exit(1)

    # check if physical user exist
    assert physical_user_name in physical_users, f"{physical_user_name} is not in the .env"
    physical_data = json.loads(physical_users[physical_user_name])
    account = physical_data["account"]
    password = physical_data["password"]


    testing_user = SecondStageTestingUser(user_options)

    # save testing user info
    testing_user_dict = vars(testing_user)
    print(testing_user_dict)
    with open(os.path.join(f"users_json/second/{testing_user.user_name}.json"), mode='w', encoding='utf-8') as f:
        json.dump(testing_user_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

    driver = webdriver.Chrome("chromedriver")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    page.second_stage_login(driver, wait, testing_user)

    sleep(1)

    # if didnt login Spotify yet
    if 'https://accounts.spotify.com/' in driver.current_url:
        page.spotify_auth(driver, wait, account, password)


    for i in range(2):
        page.song_lst_sencond(driver, wait, testing_user, testing_user.list_type[i])
        page.list_credit(driver, wait, testing_user, testing_user.list_type[i])

    print(f"Secondary Group: {testing_user.secondaryType}")
    check.check_song_lst_name_order(testing_user)

    # 以前的WD_ID與T_ID指第一次的WD_ID與T_ID
    # ------------------------------------------------
    # 以後的WD_ID與T_ID指第二次測驗的WD_ID與T_ID
    WD_ID = backend_utils.get_song_lst_id(testing_user.user_id, "Weekly_Discovery", "second")['songListID']
    T_ID = backend_utils.get_song_lst_id(testing_user.user_id, "Tags", "second")['songListID']

    testing_user.set_song_lst_id(WD_ID, "WD")
    testing_user.set_song_lst_id(T_ID, "T")

    sleep(1)

    check.check_song_lst_score(testing_user)



if __name__ == '__main__':
    main()