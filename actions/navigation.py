
from services.db_service import *
from utils.ui_factory import UIFactory
from constants import UserState
from messenger.bot import Bot

def action_welcome_user(client: Bot, user_id):
    client.send_image_url(user_id, UIFactory.IMG_LETSGO)    
    client.send_button_message(user_id, UIFactory.WELCOME_TITLE, UIFactory.get_menu_buttons())
    
    set_user_state(user_id, UserState.MENU)

def action_project_info(client: Bot, user_id):
    client.send_button_message(user_id, UIFactory.PROJECT_INTRO, UIFactory.get_project_info_btn())

    set_user_state(user_id, UserState.MENU)

def action_broken_bike_intro(client: Bot, user_id):
    client.send_button_message(user_id, UIFactory.BROKEN_BIKE_INTRO, UIFactory.get_project_info_btn())

    set_user_state(user_id, UserState.MENU)

def action_recycling_process(client: Bot, user_id):
    client.send_image_url(user_id, UIFactory.IMG_RECYCLE)
    client.send_button_message(user_id, UIFactory.RECYCLING_PROCESS, UIFactory.get_project_info_btn())
    
    set_user_state(user_id, UserState.MENU)    

def action_wrong_attachment(client: Bot, user_id):
    set_user_state(user_id, UserState.MENU)
    client.send_image_url(user_id, UIFactory.IMG_STOP)
    client.send_button_message(user_id, UIFactory.WRONG_MESSAGE, UIFactory.get_menu_buttons())
