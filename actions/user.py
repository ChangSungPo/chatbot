from services.db_service import *
from utils.ui_factory import UIFactory
from constants import UserState
from messenger.bot import Bot
from utils.validators import is_valid_taiwan_phone

def action_feedback(client: Bot, user_id):
    client.send_button_message(user_id, UIFactory.FEEDBACK, UIFactory.get_menu_buttons())

    set_user_state(user_id, UserState.FEEDBACK)

def action_change_name(client: Bot, user_id):
    client.send_button_message(user_id, UIFactory.CHANGE_NAME, UIFactory.get_back_to_menu_btn())

    set_user_state(user_id, UserState.CHANGE_NAME)

def action_change_phone_number(client: Bot, user_id):
    client.send_button_message(user_id, UIFactory.CHANGE_PHONE_NUMBER, UIFactory.get_back_to_menu_btn())

    set_user_state(user_id, UserState.CHANGE_PHONE_NUMBER)

def action_my_status(client: Bot, user_id, user_data):
    client.send_button_message(user_id, UIFactory.format_user_stats(user_data), UIFactory.get_menu_buttons())

    set_user_state(user_id, UserState.MENU)

    reports = get_user_reports(user_id)

    if not reports:
        client.send_text_message(user_id, UIFactory.NO_BIKE_REPORT)
        return
    
    for report in reports:
        text = UIFactory.format_report_item_text(report)
        btns = UIFactory.get_report_item_buttons(report)
        client.send_button_message(user_id, text, btns)    

def action_wrong_message(client: Bot, user_id):
    client.send_image_url(user_id, UIFactory.IMG_SORRY)
    client.send_button_message(user_id, UIFactory.WRONG_MESSAGE, UIFactory.get_menu_buttons())

    set_user_state(user_id, UserState.MENU)

def action_handle_feedback_text(client, user_id):
    client.send_image_url(user_id, UIFactory.IMG_GREAT)
    client.send_text_message(user_id, UIFactory.FEEDBACK_REQUEST)
    
    set_user_state(user_id, UserState.MENU)

    client.send_button_message(user_id, UIFactory.RETURN_MENU, UIFactory.get_menu_buttons())

def action_handle_user_name(client: Bot, user_id, text, user_data):
    phone = user_data.get('pnum', '<empty>')
    
    next_state = update_user_name_and_check_state(user_id, text, phone)
    
    if next_state == UserState.WAITING_FOR_PHOTO:
        text = (
            "Please send a photo of the bike/bikes you want to report.\n\n"
            f"👤 User: {text}\n"
            f"📞 Contact: {phone}"
        )
        btns = UIFactory.get_upload_prompt_buttons()
    else:
        text = (
            "You need to give your name and number to the cleaning team in order to report bikes.\n\n"
            f"👤 User: {text}\n"
            f"📞 Contact: {phone}"
        )
        btns = UIFactory.get_info_edit_buttons()
        
    client.send_button_message(user_id, text, btns)

def action_process_phone_input(client: Bot, user_id, text, user_data):
  
    # valid phone number
    if not is_valid_taiwan_phone(text):
        client.send_button_message(user_id, UIFactory.WRONG_PHONE_NUMBER, UIFactory.get_back_to_menu_btn())
        return

    name = user_data.get('namez', '<empty>')
    next_state = update_user_phone_and_check_state(user_id, text, name)

    if next_state == UserState.WAITING_FOR_PHOTO:
        text = (
            "Please send a photo of the bike/bikes you want to report.\n\n"
            f"👤 Name: {name}\n"
            f"📞 Contact: {text}"
        )
        btns = UIFactory.get_upload_prompt_buttons()
    else:
        text = (
            "You need to give your name and number to the cleaning team in order to report bikes.\n\n"
            f"👤 User: {name}\n"
            f"📞 Contact: {text}"
        )
        btns = UIFactory.get_info_edit_buttons()

    client.send_button_message(user_id, text, btns)    