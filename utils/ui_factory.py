import os
from pymessager.message import ActionButton, ButtonType

from constants import Payload

class UIFactory:
    IMG_LETSGO = os.environ.get("LETSGO")
    IMG_RECYCLE = os.environ.get("RECYCLE")
    IMG_CRY = os.environ.get("CRY")
    IMG_GREAT = os.environ["GREAT"]
    IMG_SORRY = os.environ["SORRY"]
    IMG_DOORPLATE = os.environ["DOORPLATE"]
    IMG_STOP = os.environ["STOP"]

    WELCOME_TITLE = "Welcome to BikeR's project menu, I am Cyclone, your digital assistant."
    PROJECT_INTRO = "BikeR is a pubic service project, our goal is to make the streets cleaner by reporting unused and broken bikes to the government's cleaning team. "
    BROKEN_BIKE_INTRO = "If a bike has lost parts or is extremely rusted or in other ways unusible, it is ready to be recycled. "
    RECYCLING_PROCESS = "Bike recycling process:after the cleaning team gets a report, they will investigate the report in three days, if it is acceptible for recycling, they will stick an note on the bike, if the note is still there after a week, the bike will be put in a shed, the picture of the bike will be put on a website, if the owner does not claim it, the bike will then be recycled. "
    FEEDBACK = "We respect your opinion, please write down your ideas or problems here. \n\n If you don't want to write anything, you can click the button below to go to menu. "
    FEEDBACK_REQUEST = "Your opinion is very important to us, please give us some feedback!"
    FEEDBACK_RESPONSE = "Good! The message has been sent to our team. ✅"
    CHANGE_NAME = "Please input the name. \n\nIf you don't want to change your name, press the button below to go to menu. "
    CHANGE_PHONE_NUMBER = "Please input your phone number. \n\nIf you don't want to change your number, press the button below to go to menu. "
    NO_BIKE_REPORT = "You haven't reported any bikes yet. "
    REPORT_NOT_FOUNT = "Sorry, report not found."
    PHOTO_REQUEST = "Please upload a photo of the bike/bikes you wish to report."
    REPORT_CREATED = "The report has been sent, in about a week, the cleaning team will come to check on the bike. "
    REPORT_CREATED_MANUAL = "The report has been sent to BikeR's volunteers for manual check. "
    REVIEWING_REPORT = "Thanks! Cyclone will review your report, please hold..."
    ADDRESS_ERROR = "Sorry, we couldn't verify this address. "
    WRONG_MESSAGE = "I do not understand your message.\n\n" + WELCOME_TITLE
    REQUEST_BIKE_LOCATION = "Ok, please tell me the broken bike's location. 📍"
    REQUEST_DOORPLATE_UPLOAD = "Please upload the closest doorplate image, I will use AI to recognize! 📸"
    UNKNOWN_BTN = "You have sent an unknown button! Returning to menu... "
    RETURN_MENU = "Returning to main menu..."
    WRONG_PHONE_NUMBER = "⚠️ Please input a correct phone number.\nA valid number increases your credit score!\nIf you don't want to change it, click 【To Menu】. "
    REQUEST_DOORPLATE_OR_TEXT_LOCATION = "Please upload the closest doorplate or input location in text."


    LEVEL_NAMES = [
            "rookie", "slightly advanced rookie", "level 3 apprentice", 
            "level 2 apprentice", "level 1 apprentice", "rank 9 priest", 
            "rank 8 priest", "rank 7 priest", "rank 6 priest", "rank 5 priest", 
            "rank 4 priest", "rank 3 mentor", "rank 2 mentor", "Chosen Priest", 
            "elder", "High Priest", "legendary bard", "legendary mage", 
            "illuminati follower", "illuminati priest", "illuminati"
        ]

    @staticmethod
    def get_menu_buttons():
        buttons = [
            ActionButton(ButtonType.POSTBACK, "Start Recycling", payload = Payload.START_RECYCLING),
            ActionButton(ButtonType.POSTBACK, "Project Info", payload = Payload.PROJECT_INFO),
            ActionButton(ButtonType.POSTBACK, "My Stats", payload = Payload.MY_STATS),
        ]

        return [button.to_dict() for button in buttons]

    @staticmethod
    def get_back_to_menu_btn():
        buttons = [
            ActionButton(ButtonType.POSTBACK, "To Menu", payload = Payload.TO_MENU)
        ]

        return [button.to_dict() for button in buttons]
    
    @staticmethod
    def get_project_info_btn():
        buttons = [
            ActionButton(ButtonType.POSTBACK, "To Menu", payload = Payload.TO_MENU),
            ActionButton(ButtonType.POSTBACK, "Broken Bikes?", payload = Payload.BROKEN_BIKES_INTRO),
            ActionButton(ButtonType.POSTBACK, "Recycling Process", payload = Payload.RECYCLING_PROCESS)
        ]

        return [button.to_dict() for button in buttons]
    
    @staticmethod
    def format_user_stats(user_data: dict) -> str:
        # calculate level
        credit = round(float(user_data.get('credit', 0)))
        total = int(user_data.get('totalz', 0))
        level = credit + min(total, 50) // 5

        level_name = UIFactory.LEVEL_NAMES[level] if level < len(UIFactory.LEVEL_NAMES) else "Master"

        return (
            f"👤 User: {user_data.get('name')}\n"
            f"📞 Contact: {user_data.get('pnum')}\n"
            f"⭐️ Credit: {credit}\n"
            f"🏆 Your level is: [{level_name}]\n"
            f"--------------------\n"
            f"✅ Total reported: {total}\n"
            f"♻️ Total recycled: 0\n"
            f"🚲 Pending bikes: {total}\n\n"
            f"Following are your reports:"
        )
    
    @staticmethod
    def format_report_item_text(report: dict) -> str:
        date = report.get('timestampz', '')[:10]
        addr = report.get('address', 'Unknown')
        status = report.get('status', 'N/A')
        return f"📅 Report Date: {date}\n📍 Location: {addr}\n🚦 Status: {status}"

    @staticmethod
    def get_report_item_buttons(report: dict):
        payload = report.get('timestampz')
        btns = [
            ActionButton(ButtonType.POSTBACK, "Detail", payload = payload),
            ActionButton(ButtonType.POSTBACK, "Abandon", payload = payload)
        ]
        return [b.to_dict() for b in btns]   


    @staticmethod
    def format_detail_text(report: dict) -> str:
        return (
            f"👤 User: {report.get('name')}\n"
            f"📞 Contact: {report.get('pnum')}\n"
            f"📅 Report Date: {report.get('timestampz', '')[:10]}\n"
            f"📍 Location: {report.get('address')}\n"
            f"📝 Detail: {report.get('details', '-')}\n"
            f"🚦 Status: {report.get('status')}\n"
            f"🔄 Update Date: {report.get('updatedate', '')[:10]}"
        )

    @staticmethod
    def get_detail_buttons(timestamp: str):
        btns = [
            ActionButton(ButtonType.POSTBACK, "Abandon", payload = timestamp),
            ActionButton(ButtonType.POSTBACK, "To Menu", payload = Payload.TO_MENU)
        ]
        return [b.to_dict() for b in btns]     
    
    @staticmethod
    def get_abandon_confirm_buttons(timestamp: str):

        btns = [
            ActionButton(ButtonType.POSTBACK, "Confirm Abandon", payload = timestamp),
            ActionButton(ButtonType.POSTBACK, "To Menu", payload = Payload.TO_MENU)
        ]
        return [b.to_dict() for b in btns]
    
    @staticmethod
    def get_info_request_text(name, phone):
        return (
            "The cleaning team requires you to provide your real name and number.\n\n"
            f"👤 User ID: {name}\n"
            f"📞 Contact: {phone}"
        )    
    
    @staticmethod
    def get_photo_upload_text(name, phone):
        return (
            "Please upload a photo of the bike/bikes you wish to report.\n\n"
            f"👤 User ID: {name}\n"
            f"📞 Contact: {phone}"
        )    
    
    @staticmethod
    def get_info_edit_buttons():
        btns = [
            ActionButton(ButtonType.POSTBACK, "Change Name", payload = Payload.CHANGE_NAME),
            ActionButton(ButtonType.POSTBACK, "Change Phone Number", payload = Payload.CHANGE_PHONE_NUMBER),
        ]
        return [button.to_dict() for button in btns]
    
    @staticmethod
    def get_upload_prompt_buttons():
        btns = [
            ActionButton(ButtonType.POSTBACK, "Upload Photos", payload = Payload.UPLOAD_PHOTOS),
            ActionButton(ButtonType.POSTBACK, "Change Name", payload = Payload.CHANGE_NAME),
            ActionButton(ButtonType.POSTBACK, "Change Phone Number", payload = Payload.CHANGE_PHONE_NUMBER),
        ]
        return [button.to_dict() for button in btns]

    @staticmethod
    def get_feedback_buttons():
        btns = [
            ActionButton(ButtonType.POSTBACK, "Feedback", payload = Payload.FEEDBACK),
            ActionButton(ButtonType.POSTBACK,"To Menu", payload = Payload.TO_MENU)
        ]
        return [button.to_dict() for button in btns]
    
    @staticmethod
    def get_address_detail(address: str):
        text = (
            f"📍 Address: {address}\n\n"
            "Please input your details in text (e.g., 'Behind the red gate').\n"
            "If no more details, please click the button below."
        )
        
        btns = [
            ActionButton(ButtonType.POSTBACK, "Address Correct", payload = address)
        ]

        return text, [b.to_dict() for b in btns]
    
    @staticmethod
    def get_re_detail_prompt(address: str, current_details: str):
        text = (
            f"📍 Location: {address}\n"
            f"📝 Current Detail: {current_details}\n\n"
            "Please input your new details in text.\n"
            "To use old details, please click the button below."
        )
        
        btns = [
            ActionButton(ButtonType.POSTBACK, "Address Correct", payload = address)
        ]
        return text, [b.to_dict() for b in btns]
    
    @staticmethod
    def get_score_feedback(score, name, phone, addr, details):
        if score >= 7:
            text = (
                f"Great, you will receive {score} points for this report! 🌟\n\n"
                f"👤 User: {name}\n"
                f"📞 Contact: {phone}\n"
                f"📍 Location: {addr}\n"
                f"📝 Detail: {details}"
            )

            btns = [
                ActionButton(ButtonType.POSTBACK,"Confirm Upload", payload = Payload.CONFIRM_UPLOAD),
                ActionButton(ButtonType.POSTBACK,"To Menu", payload = Payload.TO_MENU)
            ]

            return text, UIFactory.IMG_GREAT, [button.to_dict() for button in btns]
        else:
            text = (
                f"I'm sorry, this report only received {score} points. 😔\n"
                "It requires manual processing. Do you still want to send it?"
            )

            btns = [
                ActionButton(ButtonType.POSTBACK,"Manual", payload = Payload.MANUAL),
                ActionButton(ButtonType.POSTBACK,"To Menu", payload = Payload.TO_MENU)
            ]

            return text, UIFactory.IMG_CRY, [button.to_dict() for button in btns]
        
    @staticmethod
    def get_address_options(formatted_address):
        btns = [
            ActionButton(ButtonType.POSTBACK, "Confirm Address", payload = formatted_address),
            ActionButton(ButtonType.POSTBACK, "Add Detail", payload = formatted_address)
        ]
        
        text = (
            f"Is this address correct?\n📍 {formatted_address}\n\n"
            "Options:\n"
            "✅ Click 'Confirm' if correct\n"
            "📝 Click 'Add Detail' for more info\n"
            "📸 Or upload a doorplate photo"
        )
        return text, [b.to_dict() for b in btns]
    
    @staticmethod
    def get_detail_added_ui(address, detail_text):
        text = (
            "✅ Detail has been added!\n"
            f"📍 Location: {address}\n"
            f"📝 Detail: {detail_text}"
        )
        
        btns = [
            ActionButton(ButtonType.POSTBACK, "Address Correct", payload = address),
            ActionButton(ButtonType.POSTBACK, "Re-Detail", payload = address)
        ]
        return text, [b.to_dict() for b in btns]
    
    @staticmethod
    def get_bike_detection_ui(is_success):
        if is_success:
            return "✅ Bike identified!", UIFactory.IMG_GREAT, None
        else:
            text = "Oops! Cyclone couldn't recognize the bike. If you're confident it's a bike, please provide the location! 🚲"
            btns = [
                ActionButton(ButtonType.POSTBACK, "Upload Photos", payload = "Upload Photos")
            ]
            return text, UIFactory.IMG_SORRY, [button.to_dict() for button in btns]

    @staticmethod
    def get_doorplate_result_ui(address):
        if address:
            text = f"I recognized some text: {address}\nTrying to combine... 🧩"
            return text, True
        return "Oops! It doesn't seem like a doorplate. Please try again! 📸", False