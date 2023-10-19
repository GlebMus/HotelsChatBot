import telebot
import datetime
from translate import Translator
from botrequests import highpice, lowprice, bestdeal, history
from settings import *

"""
Подключение к pyTelegrambotapi
"""
bot = telebot.TeleBot(TOKEN)

""" 
Установка языков для перевода вводимых параметров 
"""
translator = Translator(from_lang="russian", to_lang="english")
translator_rus = Translator(from_lang="english", to_lang="russian")
"""
Команда start для ознакомления пользователя
"""


@bot.message_handler(commands=['start'])
def start(message: callable) -> None:
    bot.send_message(message.chat.id,
                     'Привет, команды работают! Попробуйте ввести /help для ознакомления со всеми командами')


"""
Команда help для вывода всех доступных команд
"""


@bot.message_handler(commands=['help'])
def help_func(message: callable) -> None:
    bot.send_message(message.chat.id, 'Список доступных команд:\n/highprice - Топ самых дорогих отелей в '
                                      'городе\n/lowprice - '
                                      'Топ самых дешевых отелей в городе\n/bestdeal - Топ отелей подходящих по цене и '
                                      'растоянию от центра\n/history - Вывод истории поиска (команда, дата и время вызова команды, результат поиска)')


"""
Команда history выводит историю поиска (Команда, дата и время вызова команды, результат вызова команды)
"""


@bot.message_handler(commands=['history'])
def search_city_bd(message: callable) -> None:
    try:
        bot.send_message(message.chat.id, history.history_command(message.from_user.id))
    except Exception as exp:
        logger.debug(f'Ошибка в history! (debug) \nОшибка:\n{exp}')


"""
Команда highprice выводит все отели отсортированные по убыванию цены
"""


@bot.message_handler(commands=['highprice'])
def search_city_high(message: callable) -> None:
    bot.send_message(message.chat.id, 'В каком городе искать?')
    bot.register_next_step_handler(message, how_many_high)


def how_many_high(message: callable, answer=None) -> None:
    if answer is None:
        answer = translator.translate(message.text)
        bot.send_message(message.chat.id, 'Сколько показать вариантов? (Максимум 25)')
        bot.register_next_step_handler(message, get_img_high, answer)
    else:
        bot.send_message(message.chat.id, 'Сколько показать вариантов? (Максимум 25)')
        bot.register_next_step_handler(message, get_img_high, answer)


def get_img_high(message: callable, answer: str) -> None:
    mess_anws = message.text
    if not 25 >= int(mess_anws) >= 0:
        bot.send_message(message.chat.id, 'Введите число от 0 до 25')
        how_many_high(message, answer)
    else:
        max_count = mess_anws
        bot.send_message(message.chat.id, 'Показать изображения отелей? (Да/Нет) ')
        bot.register_next_step_handler(message, how_many_img_high, answer, max_count)


def how_many_img_high(message: callable, answer: str, max_count: str) -> None:
    if message.text.lower() == 'нет':
        show_results_high_no(message, answer, max_count)
    else:
        show_results_high_yes(message, answer, max_count)


def show_results_high_no(message: callable, answer: str, max_count: str) -> None:
    highpice.ApiUrl.querystring['q'] = answer
    highpice.ApiUrl.querystring2['resultsSize'] = int(max_count)
    command = 'highprice'
    command_time = str(datetime.datetime.now())
    command_result = ''

    for i in highpice.ApiUrl.return_results():
        hotel_name = i['name']
        rating = i['reviews']['score']
        distance = i['destinationInfo']['distanceFromDestination']['value']
        distance_km = round(float(distance) * 1.6, 1)
        price = round(i['price']['lead']['amount'])
        try:
            text_for_message = f"Название отеля: {hotel_name}\nРейтинг: {rating}\nРастояние от центра: {distance} ({distance_km} KM)\nЦена: {price}$"
            bot.send_message(message.chat.id, text_for_message)
            command_result += text_for_message + '\n\n'
        except Exception as exp:
            bot.send_message(message.chat.id, 'Ошибка вывода команды')
            logger.debug(f'Ошибка вывода команды highprice!(Функция show_results_high) (debug) \nОшибка:\n{exp}')

    history.history_add(message.from_user.id, translator_rus.translate(answer), command, command_time, command_result)


def show_results_high_yes(message: callable, answer: str, max_count: str) -> None:
    highpice.ApiUrl.querystring['q'] = answer
    highpice.ApiUrl.querystring2['resultsSize'] = int(max_count)
    command = 'highprice'
    command_time = str(datetime.datetime.now())
    command_result = ''

    for i in highpice.ApiUrl.return_results():
        hotel_name = i['name']
        rating = i['reviews']['score']
        distance = i['destinationInfo']['distanceFromDestination']['value']
        distance_km = round(float(distance) * 1.6, 1)
        price = round(i['price']['lead']['amount'])

        try:
            text_for_message = f"Название отеля: {hotel_name}\nРейтинг: {rating}\nРастояние от центра: {distance} ({distance_km} KM)\nЦена: {price}$"
            bot.send_message(message.chat.id, text_for_message)

            imgs_list = []

            if i['propertyImage'].get('fallbackImage', None) is None:
                imgs_list.append(telebot.types.InputMediaPhoto(i['propertyImage']['image']['url']))
            else:
                imgs_list.extend([telebot.types.InputMediaPhoto(i['propertyImage']['fallbackImage']['url']), telebot.types.InputMediaPhoto(i['propertyImage']['image']['url'])])

            command_result += text_for_message + '\n\n'
            bot.send_media_group(message.chat.id, imgs_list)

        except Exception as exp:
            bot.send_message(message.chat.id, 'Ошибка вывода команды')
            logger.debug(
                f'Ошибка вывода команды highprice!(Функция show_results_high) (debug) \nОшибка:\n{exp}')

    history.history_add(message.from_user.id, translator_rus.translate(answer), command, command_time, command_result)


"""
Команда lowprice выводит все отели отсортированные по возрастанию цены
"""


@bot.message_handler(commands=['lowprice'])
def search_city_low(message: callable) -> None:
    bot.send_message(message.chat.id, 'В каком городе искать?')
    bot.register_next_step_handler(message, how_many_low)


def how_many_low(message: callable, answer=None) -> None:
    if answer is None:
        answer = translator.translate(message.text)
        bot.send_message(message.chat.id, 'Сколько показать вариантов? (Максимум 25)')
        bot.register_next_step_handler(message, get_img_low, answer)
    else:
        bot.send_message(message.chat.id, 'Сколько показать вариантов? (Максимум 25)')
        bot.register_next_step_handler(message, get_img_low, answer)


def get_img_low(message: callable, answer: str) -> None:
    mess_anws = message.text

    if not 25 >= int(mess_anws) >= 0:
        bot.send_message(message.chat.id, 'Введите число от 0 до 25')
        how_many_low(message, answer)
    else:
        max_count = mess_anws
        bot.send_message(message.chat.id, 'Показать изображения отелей? (Да/Нет)')
        bot.register_next_step_handler(message, how_many_img_low, answer, max_count)


def how_many_img_low(message: callable, answer: str, max_count: int) -> None:
    if message.text.lower() == 'нет':
        show_results_low_no(message, answer, max_count)
    else:
        show_results_low_yes(message, answer, max_count)


def show_results_low_no(message: callable, answer: str, max_count: int) -> None:
    lowprice.ApiUrl.querystring['q'] = answer
    lowprice.ApiUrl.querystring2['resultsSize'] = int(max_count)
    command = 'highprice'
    command_time = str(datetime.datetime.now())
    command_result = ''

    for i in lowprice.ApiUrl.return_results():
        hotel_name = i['name']
        rating = i['reviews']['score']
        distance = i['destinationInfo']['distanceFromDestination']['value']
        distance_km = round(float(distance) * 1.6, 1)
        price = round(i['price']['lead']['amount'])
        try:
            text_for_message = f"Название отеля: {hotel_name}\nРейтинг: {rating}\nРастояние от центра: {distance} ({distance_km} KM)\nЦена: {price}$"
            bot.send_message(message.chat.id, text_for_message)
            command_result += text_for_message + '\n\n'
        except Exception as exp:
            bot.send_message(message.chat.id, 'Ошибка вывода команды')
            logger.debug(f'Ошибка вывода команды lowprice!(Функция show_results_low) (debug)\nОшибка:\n{exp}')

    history.history_add(message.from_user.id, translator_rus.translate(answer), command, command_time, command_result)


def show_results_low_yes(message: callable, answer: str, max_count: int) -> None:
    lowprice.ApiUrl.querystring['q'] = answer
    lowprice.ApiUrl.querystring2['resultsSize'] = int(max_count)
    command = 'highprice'
    command_time = str(datetime.datetime.now())
    command_result = ''

    for i in lowprice.ApiUrl.return_results():
        hotel_name = i['name']
        rating = i['reviews']['score']
        distance = i['destinationInfo']['distanceFromDestination']['value']
        distance_km = round(float(distance) * 1.6, 1)
        price = round(i['price']['lead']['amount'])
        try:
            text_for_message = f"Название отеля: {hotel_name}\nРейтинг: {rating}\nРастояние от центра: {distance} ({distance_km} KM)\nЦена: {price}$"
            bot.send_message(message.chat.id, text_for_message)

            imgs_list = []

            if i['propertyImage'].get('fallbackImage', None) is None:
                imgs_list.append(telebot.types.InputMediaPhoto(i['propertyImage']['image']['url']))
            else:
                imgs_list.extend([telebot.types.InputMediaPhoto(i['propertyImage']['fallbackImage']['url']), telebot.types.InputMediaPhoto(i['propertyImage']['image']['url'])])

            command_result += text_for_message + '\n\n'
            bot.send_media_group(message.chat.id, imgs_list)

        except Exception as exp:
            bot.send_message(message.chat.id, 'Ошибка вывода команды')
            logger.debug(f'Ошибка вывода команды lowprice!(Функция show_results_low) (debug) \nОшибка:\n{exp}')

    history.history_add(message.from_user.id, translator_rus.translate(answer), command, command_time, command_result)


"""
Команда bestdeal выводит все отели отсортированные по цене и расстоянию от центра
"""


@bot.message_handler(commands=['bestdeal'])
def search_city_bd(message: callable) -> None:
    bot.send_message(message.chat.id, 'В каком городе искать?')
    bot.register_next_step_handler(message, price_range)


def price_range(message: callable) -> None:
    location = translator.translate(message.text)
    bot.send_message(message.chat.id, 'Введите минимальную и максимальную цену через пробел($)')
    bot.register_next_step_handler(message, distance_range, location)


def distance_range(message: callable, location: str) -> None:
    min_price, max_price = int(message.text.split()[0]), int(message.text.split()[1])

    if max_price < min_price:
        bot.send_message(message.chat.id, 'Вы ввели минимальное число больше максимального, мы поменяли их местами')
        min_price, max_price = max_price, min_price
        bot.send_message(message.chat.id, 'Введите минимальное и максимальное расстояние (KM)')
        bot.register_next_step_handler(message, how_many_bd, location, min_price, max_price)
    else:
        bot.send_message(message.chat.id, 'Введите минимальное и максимальное расстояние (KM)')
        bot.register_next_step_handler(message, how_many_bd, location, min_price, max_price)


def how_many_bd(message: callable, location: str, min_price: int, max_price: int, min_distance=None,
                max_distance=None) -> None:

    if min_distance is None and max_distance is None:
        min_distance, max_distance = int(message.text.split()[0]), int(message.text.split()[1])
        if max_distance < min_distance:
            bot.send_message(message.chat.id,
                             'Вы ввели минимальное число больше максимального, мы поменяли их местами')
            min_distance, max_distance = max_distance, min_distance
            bot.send_message(message.chat.id, 'Сколько показать вариантов? (Максимум 25)')
            bot.register_next_step_handler(message, get_img_bd, location, min_price, max_price, min_distance,
                                           max_distance)
        else:
            bot.send_message(message.chat.id, 'Сколько показать вариантов? (Максимум 25)')
            bot.register_next_step_handler(message, get_img_bd, location, min_price, max_price, min_distance,
                                           max_distance)
    else:
        bot.send_message(message.chat.id, 'Сколько показать вариантов? (Максимум 25)')
        bot.register_next_step_handler(message, get_img_bd, location, min_price, max_price, min_distance,
                                       max_distance)


def get_img_bd(message: callable, location: str, min_price: int, max_price: int, min_distance: int,
               max_distance: int) -> None:

    mess_anws_int = int(message.text)

    if not 25 > mess_anws_int > 0:
        bot.send_message(message.chat.id, 'Введите число от 0 до 25')
        how_many_bd(message, location, min_price, max_price, min_distance, max_distance)
    else:
        max_count = message.text
        bot.send_message(message.chat.id, 'Показать изображения отелей?(Да/Нет) ')
        bot.register_next_step_handler(message, how_many_img_bd, location, min_price, max_price, min_distance,
                                       max_distance, max_count)


def how_many_img_bd(message: callable, location: str, min_price: int, max_price: int, min_distance: int,
                    max_distance: int, max_count: str) -> None:

    if message.text.lower() == 'нет':
        show_results_bd_no(message, location, min_price, max_price, min_distance, max_distance, max_count)
    else:
        show_results_bd_yes(message, location, min_price, max_price, min_distance, max_distance, max_count)


def show_results_bd_no(message: callable, location: str, min_price: int, max_price: int, min_distance: int,
                       max_distance: int, max_count: str) -> None:

    bestdeal.ApiUrl.querystring['q'] = location
    bestdeal.ApiUrl.querystring2['resultsSize'] = int(max_count)
    bestdeal.ApiUrl.querystring2['filters']['price']['max'] = int(max_price)
    bestdeal.ApiUrl.querystring2['filters']['price']['min'] = int(min_price)
    command = 'bestdeal'
    command_time = str(datetime.datetime.now())
    command_result = ''

    for i in bestdeal.ApiUrl.return_results():
        hotel_name = i['name']
        rating = i['reviews']['score']
        distance = i['destinationInfo']['distanceFromDestination']['value']
        distance_km = round(float(distance) * 1.6, 1)
        price = round(i['price']['lead']['amount'])
        try:
            if min_distance < distance_km < max_distance:
                text_for_message = f"Название отеля: {hotel_name}\nРейтинг: {rating}\nРастояние от центра: {distance} ({distance_km} KM)\nЦена: {price}$"
                bot.send_message(message.chat.id, text_for_message)
                command_result += text_for_message + "\n\n"
        except Exception as exp:
            bot.send_message(message.chat.id, 'Ошибка вывода команды')
            logger.debug(f'Ошибка вывода команды bestdeal!(Функция show_results_bd) (debug)\nОшибка:\n{exp}')

    history.history_add(message.from_user.id, translator_rus.translate(location), command, command_time, command_result)


def show_results_bd_yes(message: callable, location: str, min_price: int, max_price: int, min_distance: int,
                        max_distance: int, max_count: str) -> None:

    bestdeal.ApiUrl.querystring['q'] = location
    bestdeal.ApiUrl.querystring2['resultsSize'] = int(max_count)
    bestdeal.ApiUrl.querystring2['filters']['price']['max'] = int(max_price)
    bestdeal.ApiUrl.querystring2['filters']['price']['min'] = int(min_price)
    command = 'bestdeal'
    command_time = str(datetime.datetime.now())
    command_result = ''

    for i in bestdeal.ApiUrl.return_results():
        hotel_name = i['name']
        rating = i['reviews']['score']
        distance = i['destinationInfo']['distanceFromDestination']['value']
        distance_km = round(float(distance) * 1.6, 1)
        price = round(i['price']['lead']['amount'])
        try:
            if min_distance < distance_km < max_distance:
                text_for_message = f"Название отеля: {hotel_name}\nРейтинг: {rating}\nРастояние от центра: {distance} ({distance_km} KM)\nЦена: {price}$"
                bot.send_message(message.chat.id, text_for_message)
                imgs_list = []

                if i['propertyImage'].get('fallbackImage', None) is None:
                    imgs_list.append(telebot.types.InputMediaPhoto(i['propertyImage']['image']['url']))
                else:
                    imgs_list.extend([telebot.types.InputMediaPhoto(i['propertyImage']['fallbackImage']['url']),
                                      telebot.types.InputMediaPhoto(i['propertyImage']['image']['url'])])

                command_result += text_for_message + "\n\n"
                bot.send_media_group(message.chat.id, imgs_list)
        except Exception as exp:
            bot.send_message(message.chat.id, 'Ошибка вывода команды')
            logger.debug(f'Ошибка вывода команды bestdeal!(Функция show_results_bd) (debug)\nОшибка:\n{exp}')

    history.history_add(message.from_user.id, translator_rus.translate(location), command, command_time, command_result)


bot.infinity_polling()
