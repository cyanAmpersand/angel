import re

def is_valid_hex(hex):
    match3 = re.match("[a-fA-F0-9]{3}",hex.strip())
    match6 = re.match("[a-fA-F0-9]{6}", hex.strip())
    if match3 is not None:
        return True
    if match6 is not None:
        return True
    return False


def get_hex_image(valid_hex):
    hex = valid_hex.strip().upper()
    url = "https://dummyimage.com/200x200/" + hex + "/000000.png&text=" + hex
    return url

def invert(valid_hex):
    table = string.maketrans('0123456789abcdef', 'fedcba9876543210')
    return '#' + valid_hex[1:].lower().translate(table).upper()