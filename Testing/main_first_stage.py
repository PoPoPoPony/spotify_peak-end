from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from options import get_first_stage_user_options
import page
from testing_user import FirstStageTestingUser
import check
import backend_utils
import os
import json
from dotenv import dotenv_values


def main():
    physical_users = dotenv_values(".env")
    user_options = get_first_stage_user_options()
    
    # check if physical user exist
    assert user_options.physical_user_name in physical_users, f"{user_options.physical_user_name} is not in the .env"
    physical_data = json.loads(physical_users[user_options.physical_user_name])
    account = physical_data["account"]
    password = physical_data["password"]

    testing_user = FirstStageTestingUser(user_options)
    
    # save testing user info
    testing_user_dict = vars(testing_user)
    with open(os.path.join(f"users_json/first/{testing_user.user_name}.json"), mode='w', encoding='utf-8') as f:
        json.dump(testing_user_dict, f, indent=4, sort_keys=True, ensure_ascii=False)


    driver = webdriver.Chrome("chromedriver")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    page.first_stage_login(driver, wait, testing_user)

    # if didnt login Spotify yet
    if 'https://accounts.spotify.com/' in driver.current_url:
        page.spotify_auth(driver, wait, account, password)

    # only first stage will do exercise
    page.exercise(driver, wait)

    for i in range(2):
        if testing_user.list_type[i] == 'WD':
            sleep(1)
            elem = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/button')
            elem.click()
            if testing_user.UI[i] == 'list':
                page.song_lst_list(driver, wait, testing_user, 'WD')
            elif testing_user.UI[i] == 'single':
                page.song_lst_single(driver, wait, testing_user, "WD")

        elif testing_user.list_type[i] == 'T':
            sleep(10)
            page.select_tags(driver, wait, testing_user)
            if testing_user.UI[i] == 'list':
                page.song_lst_list(driver, wait, testing_user, 'T')
            elif testing_user.UI[i] == 'single':
                page.song_lst_single(driver, wait, testing_user, "T")

        page.list_credit(driver, wait, testing_user, testing_user.list_type[i])


    check.check_group(testing_user)
    user_id = backend_utils.get_users(testing_user.email)['userID']
    testing_user.set_user_id(user_id)

    WD_ID = backend_utils.get_song_lst_id(testing_user.user_id, "Weekly_Discovery", "first")['songListID']
    T_ID = backend_utils.get_song_lst_id(testing_user.user_id, "Tags", "first")['songListID']
    testing_user.set_song_lst_id(WD_ID, "WD")
    testing_user.set_song_lst_id(T_ID, "T")

    sleep(1)

    check.check_song_lst_elem(testing_user)
    check.check_song_lst_score(testing_user)
    check.check_tags(testing_user)



if __name__ == '__main__':
    main()