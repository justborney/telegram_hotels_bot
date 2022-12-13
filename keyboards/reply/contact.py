from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_user_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("Отправить контакт", request_contact=True))
    return keyboard
