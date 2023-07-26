from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
from random import randint
import utils


def first_stage_login(driver, wait, testing_user):
    driver.get("http://ponyia.ddns.net:8081/")

    user_email_input = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        '//*[@id="panel_elem"]/div[2]/div/input'
    )))

    user_email_input.clear()
    user_email_input.send_keys(testing_user.email)

    if testing_user.first_stage_group<=4: 
        row_idx=5 # first row's xpath
        col_idx = testing_user.first_stage_group
    else:
        row_idx=6 # second row's xpath
        col_idx = testing_user.first_stage_group-4


    group_btn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f'//*[@id="panel_elem"]/div[{row_idx}]/div[{col_idx}]/div/label/span')
        )
    ) # 等待元素出現
    group_btn.click()

    start_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="panel_elem"]/div[7]/div/button'))) # 等待元素出現

    start_btn.click()


def spotify_auth(driver, wait, account, password):
    #輸入spotify授權頁面之帳密
    spotify_email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-username"]'))) # 等待元素出現
    spotify_email.clear()
    spotify_email.send_keys(account)
    spotify_pwd = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-password"]'))) # 等待元素出現
    spotify_pwd.clear()
    spotify_pwd.send_keys(password)
    login_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-button"]/span[1]'))) # 等待元素出現
    login_btn.click()



def exercise(driver, wait):
    for row_i in range(1, 4):
        # 只有第一次需要等待loading instance
        if row_i == 1:
            sleep(3) 

        plyr_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[4]/div/button')
            )
        )

        plyr_btn.click()
        sleep(1)

        for col_i in range(5, 7): # xpath for sliders is 5 and 6
            bar = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[{col_i}]/div/div/div')
                )
            )

            utils.drag_slider(driver, bar, randint(1, 10), slider_max=10)

        complete_single_btn = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[7]/div/button')
        complete_single_btn.click()

    start_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="app"]/div/div[3]/div/button')
        )
    )

    # wait for api passing data
    sleep(3)

    # testing
    # sleep(1000000)

    start_btn.click()



def song_lst_list(driver, wait, testing_user, list_type):
    # setting xpath index
    player_col_i = 4
    like_slider_col_i = 5
    splendid_slider_col_i = 6

    # 若有"收藏"欄位，則column的index不同
    if testing_user.is_add:
        added_col_i = 7
        complete_col_i = 8
    else:
        added_col_i = -1
        complete_col_i = 7

    if list_type == 'WD':
        like_scores = testing_user.weekly_like_scores
        splendid_scores = testing_user.weekly_splendid_scores
        added_lst = testing_user.weekly_song_lst_added
        listened_lst = testing_user.weekly_listened
    elif list_type == 'T':
        like_scores = testing_user.tag_like_scores
        splendid_scores = testing_user.tag_splendid_scores
        added_lst = testing_user.tag_song_lst_added
        listened_lst = testing_user.tag_listened

    for row_i in range(1, 21):
        if row_i == 1:
            sleep(3) # waiting for loading instance

        # if row_i%4==0:
        #     body = driver.find_element(By.CSS_SELECTOR, 'body')
        #     body.send_keys(Keys.PAGE_DOWN)
        #     sleep(1)


        plyr_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[{player_col_i}]/div/button')
            )
        )


        plyr_pos_info = plyr_btn.rect
        plyr_pos_info_y = plyr_pos_info['y']

        script = f"window.scrollTo(0, {plyr_pos_info_y-200});"
        driver.execute_script(script)

        plyr_btn.click()
        sleep(1)

        like_bar = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[{like_slider_col_i}]/div/div/div')
            )
        )

        utils.drag_slider(driver, like_bar, like_scores[row_i-1], slider_max=10)

        splendid_bar = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[{splendid_slider_col_i}]/div/div/div')
            )
        )
        utils.drag_slider(driver, splendid_bar, splendid_scores[row_i-1], slider_max=10)

        # if in add group and need added
        if added_col_i!=-1 and row_i-1 in added_lst:
            splendid_slider_container = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[{splendid_slider_col_i}]')

            # 不知道為啥定位是錯誤的，只能用pixel指定位置再click，因此只適用於1920*1080的螢幕
            utils.checked_checkbox(driver, splendid_slider_container, "right", 50)

        # if need listened 
        if row_i-1 in listened_lst:
            song_name_container = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[2]')

            # 不知道為啥定位是錯誤的，只能用pixel指定位置再click，因此只適用於1920*1080的螢幕
            utils.checked_checkbox(driver, song_name_container, "left", -60)

        complete_elem = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[{row_i}]/td[{complete_col_i}]/div/button')
        complete_elem.click()

    sleep(1)
    send_btn = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[3]/div/button')
    send_btn.click()

    send_confirm_btn = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[5]/div/div/div[3]/span/button[2]')
    send_confirm_btn.click()


def song_lst_single(driver, wait, testing_user, list_type):
    # setting xpath index
    player_col_i = 4
    like_slider_col_i = 5
    splendid_slider_col_i = 6

    # 若有"收藏"欄位，則column的index不同
    if testing_user.is_add:
        added_col_i = 7
        complete_col_i = 8
    else:
        added_col_i = -1
        complete_col_i = 7

    if list_type == 'WD':
        like_scores = testing_user.weekly_like_scores
        splendid_scores = testing_user.weekly_splendid_scores
        added_lst = testing_user.weekly_song_lst_added
        listened_lst = testing_user.weekly_listened
    elif list_type == 'T':
        like_scores = testing_user.tag_like_scores
        splendid_scores = testing_user.tag_splendid_scores
        added_lst = testing_user.tag_song_lst_added
        listened_lst = testing_user.tag_listened

    for i in range(20):
        sleep(1.5)

        plyr_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[1]/td[{player_col_i}]/div/button')
            )
        )

        plyr_btn.click()
        sleep(1)

        like_bar = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[1]/td[{like_slider_col_i}]/div/div/div')
            )
        )

        utils.drag_slider(driver, like_bar, like_scores[i], slider_max=10)

        splendid_bar = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[1]/td[{splendid_slider_col_i}]/div/div/div')
            )
        )
        utils.drag_slider(driver, splendid_bar, splendid_scores[i], slider_max=10)

        # if in add group and need added
        if added_col_i!=-1 and i in added_lst:
            splendid_slider_container = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[1]/td[{splendid_slider_col_i}]')

            # 不知道為啥定位是錯誤的，只能用pixel指定位置再click，因此只適用於1920*1080的螢幕
            utils.checked_checkbox(driver, splendid_slider_container, "right", 50)

        # if need listened 
        if i in listened_lst:
            song_name_container = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[1]/td[2]')

            # 不知道為啥定位是錯誤的，只能用pixel指定位置再click，因此只適用於1920*1080的螢幕
            utils.checked_checkbox(driver, song_name_container, "left", -60)

        complete_elem = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[1]/td[{complete_col_i}]/div/button')
        complete_elem.click()




def list_credit(driver, wait, testing_user, list_type):
    # scores's order need to be same as the web page
    if list_type == 'WD':
        scores = [
            testing_user.weekly_satisfy,
            testing_user.weekly_diversity,
            testing_user.weekly_novelty
        ]
    elif list_type == 'T':
        scores = [
            testing_user.tag_satisfy,
            testing_user.tag_diversity,
            testing_user.tag_novelty
        ]

    sleep(3) # waiting for animation

    for row_i in range(1, 4):
        bar = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="credit_container"]/div[{row_i}]/div[2]/div/div')
            )
        )
        utils.drag_slider(driver, bar, scores[row_i-1], slider_max=10)

    send_btn = driver.find_element(By.XPATH, f'//*[@id="send_btn"]')
    send_btn.click()


def select_tags(driver, wait, testing_user):
    tags = testing_user.tags

    for i, tag_i in enumerate(tags):
        tag = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="tagTable_container"]/div/div[1]/div[3]/table/tbody/tr[{i+1}]/td[2]/div/div/label[{tag_i+1}]')
            )
        )

        tag.click()

    sleep(1)
    send_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="tagTable_container"]/div/div[2]/div[2]/button[2]')
        )
    )


    send_btn.click()



def second_stage_login(driver, wait, testing_user):
    driver.get("http://ponyia.ddns.net:8081/")

    user_email_input = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        '//*[@id="panel_elem"]/div[2]/div/input'
    )))

    user_email_input.clear()
    user_email_input.send_keys(testing_user.email)
    user_email_input.send_keys(Keys.ENTER)

    start_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="panel_elem"]/div[3]/div/button')
        )
    )

    start_btn.click()

def song_lst_sencond(driver, wait, testing_user, list_type):
    # setting xpath index
    song_name_i = 2
    player_col_i = 4
    complete_col_i = 5

    song_names = []
    for i in range(20):
        plyr_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[1]/td[{player_col_i}]/div/button')
            )
        )
        song_names.append(driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr/td[{song_name_i}]/div').text)
        plyr_btn.click()
        sleep(3)

        # [0720] 更新，現在不需要點"完成"
        # complete_elem = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[2]/div/div/div/div[3]/table/tbody/tr[1]/td[{complete_col_i}]/div/button')
        # complete_elem.click()

    if list_type == 'WD':
        testing_user.IN_WD_names = song_names
    elif list_type == 'T':
        testing_user.IN_T_names = song_names