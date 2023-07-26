from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from random import randint
from time import sleep


def drag_slider(driver, bar, score, slider_max):
    pos_info = bar.rect
    bar_x = pos_info['x']
    bar_y = pos_info['y']
    bar_w= pos_info['width']
    bar_h = pos_info['height']

    # 有時候score太小時，位置被拉桿佔據，會無法移動(click)
    if score < slider_max*0.2:
        temp_score = score+slider_max*0.3
        drag_slider(driver, bar, temp_score, slider_max)

    x = bar_x+(bar_w/slider_max)*score
    y = bar_y+bar_h/2

    if x >= (bar_x+bar_w)*0.99999:
        x = (bar_x+bar_w)*0.99998

    # because of page down
    script = "return window.pageYOffset;"
    offset_y = driver.execute_script(script)

    actions = ActionBuilder(driver)
    actions.pointer_action.move_to_location(
        x,
        y-offset_y
    )
    actions.perform()

    actions = ActionChains(driver)
    actions.click().perform()


def checked_checkbox(driver, relative_container, offset_side, offset_from_relative_x):
    pos_info = relative_container.rect
    container_x = pos_info['x']
    container_y = pos_info['y']
    container_w= pos_info['width']
    container_h = pos_info['height']


    add_checkbox_x = container_x+offset_from_relative_x
    if offset_side == 'right':
        add_checkbox_x+=container_w

    add_checkbox_y = container_y+container_h/2

    # because of page down
    script = "return window.pageYOffset;"
    offset_y = driver.execute_script(script)

    actions = ActionBuilder(driver)
    actions.pointer_action.move_to_location(
        add_checkbox_x,
        add_checkbox_y-offset_y
    )
    actions.perform()

    actions = ActionChains(driver)
    actions.click().perform()
















