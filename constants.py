
from enum import Enum

class Payload(str, Enum):
    GET_STARTED_PAYLOAD = "GET_STARTED_PAYLOAD"
    GET_STARTED = "Get Started"
    TO_MENU = "To Menu"
    START_RECYCLING = "Start Recycling"
    PROJECT_INFO = "Project Info"
    MY_STATS = "My Stats"
    BROKEN_BIKES_INTRO = "Broken Bikes?"
    RECYCLING_PROCESS = "Recycling Process"
    FEEDBACK = "Feedback"
    CHANGE_NAME = "Change Name"
    CHANGE_PHONE_NUMBER = "Change Phone Number"
    MY_STATUS = "My Stats"
    REPORT_DETAIL = "Detail"
    ADD_DETAIL = "Add Detail"
    ABANDON = "Abandon"
    CONFIRM_ABANDON = "Confirm Abandon"
    UPLOAD_PHOTOS = "Upload Photos"
    CONFIRM_UPLOAD = "Confirm Upload"
    MANUAL = "Manual"
    RE_DETAIL = "Re-Detail"
    ADDRESS_CORRECT = "Address Correct"

    TEXT_ADDRESS = "text_address"
    DOORPLATE = "doorplate"


class UserState(int, Enum):
    MENU = 0
    CHANGE_NAME = 1
    CHANGE_PHONE_NUMBER = 2
    WAITING_FOR_PHOTO = 3
    UPLOADING_PHOTO = 4
    ADDRESS_CONFIRMATION = 5
    CONFIRMING_REPORT = 6
    FEEDBACK = 7
    WAITING_FOR_DETAILS = 8