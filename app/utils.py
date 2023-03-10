from random import randint
from datetime import datetime

import requests as requests
import shutil

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
ALLOWED_EXTENSIONS = {'png', 'jpg'}


def time_now(with_seconds=True, input_format=False):
    result = datetime.now().strftime("%d.%m.%Y %H:%M")
    if input_format:
        result = datetime.now().strftime("%Y-%m-%dT%H:%M")
    if with_seconds:
        result += datetime.now().strftime(".%S")
    return result


def generate_string(length=6, alphabet=None):
    if alphabet is None:
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I",
                    "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                    "S", "T", "U", "V", "W", "X", "Y", "Z", "0",
                    "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    result = ""
    for i in range(length):
        result += alphabet[randint(0, len(alphabet) - 1)]
    return result


def get_picture(url, save_path):
    response = requests.get(url, stream=True, headers={'user-agent': USER_AGENT})

    response.raw.decode_content = True
    with open(save_path, "wb") as file:
        shutil.copyfileobj(response.raw, file)


def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
