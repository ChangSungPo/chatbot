
from services.db_service import *
from utils.ui_factory import UIFactory
from messenger.bot import Bot

def action_show_report_detail(client: Bot, user_id, timestamp):
    report = get_report_by_timestamp(user_id, timestamp)
    
    if not report:
        client.send_text_message(user_id, UIFactory.REPORT_NOT_FOUNT)
        return

    if report.get('bikephoto'):
        client.send_image_url(user_id, report['bikephoto'])
    
    detail_text = UIFactory.format_detail_text(report)
    btns = UIFactory.get_detail_buttons(timestamp)
    
    client.send_button_message(user_id, detail_text, btns)

def action_initiate_abandon(client: Bot, user_id, timestamp):
    report = get_report_by_timestamp(user_id, timestamp)
    
    if not report:
        client.send_text_message(user_id, UIFactory.REPORT_NOT_FOUNT)
        return

    client.send_image_url(user_id, UIFactory.IMG_CRY)
    client.send_button_message(user_id, "Abandon report?", UIFactory.get_abandon_confirm_buttons(timestamp))

def action_confirm_abandon(client: Bot, user_id, timestamp, user_data):
    current_total = int(user_data.get('totalz', 0))
    
    success = execute_report_abandonment(user_id, timestamp, current_total)
    
    if success:
        client.send_button_message(user_id, "Report deleted successfully", UIFactory.get_back_to_menu_btn())
    else:
        client.send_text_message(user_id, UIFactory.REPORT_NOT_FOUNT)