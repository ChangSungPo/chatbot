
def is_valid_taiwan_phone(phone_text: str) -> bool:
    return len(phone_text) == 10 and phone_text.startswith("09")