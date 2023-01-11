from random import randint
from datetime import datetime


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
