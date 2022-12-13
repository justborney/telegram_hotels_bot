from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message
from keyboards.reply.contact import request_user_contact


@bot.message_handler(commands=["survey"])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(
        message.from_user.id, f"Привет, {message.from_user.username}. Введи свое имя"
    )


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Записано. Введи возраст")
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
            user_data["name"] = message.text
    else:
        bot.send_message(message.from_user.id, "Неверное имя")


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Записано. Введи страну проживания")
        bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
            user_data["age"] = message.text
    else:
        bot.send_message(message.from_user.id, "Неверный возраст")


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    bot.send_message(message.from_user.id, "Записано. Введи город")
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
        user_data["country"] = message.text


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    bot.send_message(
        message.from_user.id,
        "Записано. Отрправь свой номер нажав на кнопку",
        reply_markup=request_user_contact(),
    )
    bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
        user_data["city"] = message.text


@bot.message_handler(
    content_types=["text", "contact"], state=UserInfoState.phone_number
)
def get_contact(message: Message) -> None:
    if message.content_type == "contact":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as user_data:
            user_data["phone_number"] = message.contact.phone_number

            reply_text = f"""Спасибо за предоставленную информацию. Ваши данные:\n
            Имя: {user_data['name']}
            Возраст: {user_data['age']}
            Страна: {user_data['country']}
            Город: {user_data['city']}
            Номер телефона: {user_data['phone_number']}"""

            bot.send_message(message.from_user.id, reply_text)
    else:
        bot.send_message(message.from_user.id, "Нажмите на кнопку")
