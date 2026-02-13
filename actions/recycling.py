from services.ai_service import *
from services.db_service import *
from services.map_services import *
from utils.scoring import calculate_address_score
from utils.ui_factory import UIFactory
from constants import Payload, UserState
from messenger.bot import Bot

def action_start_recycling(client: Bot, user_id, user_data):
    name = user_data.get('namez', '<empty>')
    phone = user_data.get('pnum', '<empty>')

    if name == '<empty>' or phone == '<empty>':
        text = UIFactory.get_info_request_text(name, phone)
        client.send_button_message(user_id, text, UIFactory.get_info_edit_buttons())
    else:
        text = UIFactory.get_photo_upload_text(name, phone)
        client.send_button_message(user_id, text, UIFactory.get_upload_prompt_buttons())
        
        set_user_state(user_id, UserState.WAITING_FOR_PHOTO)

def action_upload_photos(client: Bot, user_id):
    client.send_text_message(user_id, UIFactory.PHOTO_REQUEST)
    set_user_state(user_id, UserState.UPLOADING_PHOTO)

def action_finalize_report(client: Bot, user_id, user_data, is_manual = False):
    # calculate credit
    score = int(user_data.get('score', 0))
    credit = float(user_data.get('credit', 0))
    total = int(user_data.get('totalz', 0))
    
    final_credit = (score + (credit * total)) / (total + 1)

    # create report and update user report count
    submit_final_report(user_id, user_data, final_credit)

    if not is_manual:
        msg = UIFactory.REPORT_CREATED
    else:
        msg = UIFactory.REPORT_CREATED_MANUAL
    
    client.send_text_message(user_id, msg)

    text = UIFactory.FEEDBACK_REQUEST
    btn = UIFactory.get_feedback_buttons()
    client.send_button_message(user_id, text, btn)

def action_request_address_details(client: Bot, recipient_id, address):
    text, btns = UIFactory.get_address_detail(address)
    
    client.send_button_message(recipient_id, text, btns)
    
    set_user_state(recipient_id, UserState.WAITING_FOR_DETAILS)

def action_re_request_details(client: Bot, user_id, address, user_data):
    current_details = user_data.get('details', 'None')
    
    text, btns = UIFactory.get_re_detail_prompt(address, current_details)
    
    client.send_button_message(user_id, text, btns)    

def action_verify_address_and_score(client: Bot, user_id, address, user_data):
    client.send_text_message(user_id, UIFactory.REVIEWING_REPORT)

    geo = get_address_details(address, os.getenv("GOOGLE_API_KEY"))
    if not geo:
        client.send_text_message(user_id, UIFactory.ADDRESS_ERROR)
        return

    addr = geo['formatted_address']
    score = calculate_address_score(addr, geo['is_route'], geo['is_street_number'])

    update_report_score_state(user_id, score, addr, lat = 0, lng = 0)

    feedback_text, img, btns = UIFactory.get_score_feedback(
        score, user_data['namez'], user_data['pnum'], addr, user_data.get('details', '')
    )
    
    client.send_image_url(user_id, img)
    client.send_button_message(user_id, feedback_text, btns)  


def action_handle_address_method(client: Bot, user_id, method):
    if method == Payload.TEXT_ADDRESS:
        client.send_text_message(user_id, UIFactory.REQUEST_BIKE_LOCATION)
    elif method == Payload.DOORPLATE:
        client.send_image_url(user_id, UIFactory.IMG_DOORPLATE)
        client.send_text_message(user_id, UIFactory.REQUEST_DOORPLATE_UPLOAD)
    else:
        client.send_image_url(user_id, UIFactory.IMG_SORRY)
        client.send_button_message(user_id, UIFactory.UNKNOWN_BTN, UIFactory.get_menu_buttons())
        set_user_state(user_id, UserState.MENU)

def action_handle_text_address(client: Bot, user_id, input_text):
    client.send_text_message(user_id, "Thanks! Cyclone will use AI to organize, please hold... 🤖")

    geo = get_address_details(input_text, os.getenv("GOOGLE_API_KEY"))

    if geo:
        formatted_addr = geo['formatted_address']
        update_user_temp_address(user_id, formatted_addr)

        text, btns = UIFactory.get_address_options(formatted_addr)
        client.send_text_message(user_id, formatted_addr)
        client.send_button_message(user_id, text, btns)
    else:
        client.send_image_url(user_id, UIFactory.IMG_SORRY)
        client.send_text_message(
            user_id, 
            "Cyclone couldn't understand your address. 😵‍💫\n"
            "You could re-input it or upload a doorplate photo!"
        )        

def action_handle_address_details(client: Bot, user_id, input_text, user_data):
    update_user_location_details(user_id, input_text)
    
    current_address = user_data.get('address', 'Unknown Location')
    
    confirm_text, btns = UIFactory.get_detail_added_ui(current_address, input_text)
    client.send_button_message(user_id, confirm_text, btns)

def action_handle_bike_photo(client: Bot, user_id, photo_url, user_item):
    # check user data
    if user_item.get('namez') == '<empty>' or user_item.get('pnum') == '<empty>':
        client.send_image_url(user_id, UIFactory.IMG_STOP)
        client.send_button_message(user_id, "Name/Number required!", UIFactory.get_info_edit_buttons())
        return

    # detect bike
    client.send_text_message(user_id, "Photo received, identifying... 🧐")
    has_bike = detect_bicycle_in_image(photo_url)
    
    update_user_photo_result(user_id, photo_url, has_bike)
    text, img, btn = UIFactory.get_bike_detection_ui(has_bike)
    
    client.send_image_url(user_id, img)
    if btn: 
        client.send_button_message(user_id, text, btn)
    else: 
        client.send_text_message(user_id, text)
    
    # ask address
    client.send_text_message(user_id, UIFactory.REQUEST_DOORPLATE_OR_TEXT_LOCATION)

def action_handle_doorplate_photo(client: Bot, user_id, photo_url):
    # doorplate photo
    client.send_text_message(user_id, "Got it! Analyzing doorplate... 📸")
    
    raw_addr = recognize_doorplate_text(photo_url)
    text, is_success = UIFactory.get_doorplate_result_ui(raw_addr)
    client.send_text_message(user_id, text)

    if is_success:
        geo = get_address_details(raw_addr, os.getenv("GOOGLE_API_KEY"))
        if geo:
            formatted_addr = geo['formatted_address']
            update_user_temp_address(user_id, formatted_addr)
            
            prompt, btns = UIFactory.get_address_options(formatted_addr)
            client.send_text_message(user_id, formatted_addr)
            client.send_button_message(user_id, prompt, btns)
        else:
            client.send_text_message(user_id, "Information not enough, please try again or type the address.")    