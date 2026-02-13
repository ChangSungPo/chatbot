import os
import json

from actions.navigation import *
from actions.recycling import *
from actions.reports import *
from actions.user import *
from constants import Payload
from services.db_service import *
from dotenv import load_dotenv

from messenger.bot import Bot

client = Bot(os.environ['ACCESS_TOKEN'])
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def handle_event(messaging_event): 
    user_id = messaging_event["sender"]["id"]
    user_data = get_user_data(user_id)
    if not user_data:
        user_data = initialize_user(user_id)

    if "postback" in messaging_event:
        postback_data = messaging_event["postback"]
        handle_postback(user_id, postback_data, user_data)
    elif "message" in messaging_event and "quick_reply" in messaging_event["message"]:
        user_state = user_data.get('state', UserState.MENU)
        payload = messaging_event["message"]["quick_reply"].get("payload")

        if user_state == UserState.ADDRESS_CONFIRMATION:
            action_handle_address_method(client, user_id, payload)
    elif "message" in messaging_event and "text" in messaging_event["message"]:
        handle_message(user_id, messaging_event["message"], user_data)
    elif "message" in messaging_event:
        handle_attachments(user_id, messaging_event["message"]["attachments"], user_data)

def handle_postback(user_id, postback_data, user_data):
    action_title = postback_data["title"]
    user_state = user_data["state"]

    if action_title in (Payload.TO_MENU, Payload.GET_STARTED):
        action_welcome_user(client, user_id)
    elif action_title == Payload.PROJECT_INFO:
        action_project_info(client, user_id)
    elif action_title == Payload.BROKEN_BIKES_INTRO:
        action_broken_bike_intro(client, user_id)
    elif action_title == Payload.RECYCLING_PROCESS:
        action_recycling_process(client, user_id)
    elif action_title == Payload.FEEDBACK:
        action_feedback(client, user_id)
    elif action_title == Payload.CHANGE_NAME:
        action_change_name(client, user_id)
    elif action_title == Payload.CHANGE_PHONE_NUMBER:
        action_change_phone_number(client, user_id)
    elif action_title == Payload.MY_STATUS:
        action_my_status(client, user_id, user_data)
    elif action_title == Payload.REPORT_DETAIL:
        payload = postback_data["payload"]
        action_show_report_detail(client, user_id, payload)
    elif action_title == Payload.ABANDON:
        payload = postback_data["payload"]
        action_initiate_abandon(client, user_id, payload)
    elif action_title == Payload.CONFIRM_ABANDON:
        payload = postback_data["payload"]
        action_confirm_abandon(client, user_id, payload, user_data)
    elif action_title == Payload.START_RECYCLING:
        action_start_recycling(client, user_id, user_data)
    elif action_title == Payload.UPLOAD_PHOTOS:
        action_upload_photos(client, user_id)
    elif user_state == UserState.CONFIRMING_REPORT and (action_title == Payload.CONFIRM_UPLOAD or action_title == Payload.MANUAL):
        action_finalize_report(client, user_id, user_data)
    elif user_state == UserState.ADDRESS_CONFIRMATION and action_title == Payload.ADD_DETAIL:
        payload = postback_data["payload"]
        action_request_address_details(client, user_id, payload)
    elif user_state == UserState.WAITING_FOR_DETAILS and action_title == Payload.RE_DETAIL:
        payload = postback_data["payload"]
        action_re_request_details(client, user_id, payload, user_data)
    elif user_state in (UserState.WAITING_FOR_DETAILS, UserState.ADDRESS_CONFIRMATION) and action_title == Payload.ADDRESS_CORRECT:
        payload = postback_data["payload"]
        action_verify_address_and_score(client, user_id, payload, user_data)
    else:
        action_wrong_message(client, user_id)

def handle_message(user_id, message, user_data):
    user_state = user_data["state"]
    text = message["text"]
    if text:
        if user_state == UserState.FEEDBACK:
            action_handle_feedback_text(client, user_id)
        elif user_state == UserState.CHANGE_NAME:
            action_handle_user_name(client, user_id, text, user_data)
        elif user_state == UserState.CHANGE_PHONE_NUMBER:
            action_process_phone_input(client, user_id, text, user_data)
        elif user_state == UserState.ADDRESS_CONFIRMATION:
            action_handle_text_address(client, user_id, text)
        elif user_state == UserState.WAITING_FOR_DETAILS:
            action_handle_address_details(client, user_id, text, user_data)
        else:
            action_welcome_user(client, user_id)

def handle_attachments(user_id, attachments, user_data):
    user_state = user_data.get('state', UserState.MENU)
    
    for att in attachments:
        if att["type"] != "image":
            continue
            
        url = att["payload"]["url"]
        
        if user_state in [UserState.MENU, UserState.WAITING_FOR_PHOTO, UserState.UPLOADING_PHOTO]:
            action_handle_bike_photo(client, user_id, url, user_data)
        elif user_state == UserState.ADDRESS_CONFIRMATION:
            action_handle_doorplate_photo(client, user_id, url)
        else:
            action_wrong_message(client, user_id)
