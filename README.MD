## Цель проекта:

Создать чат бот для вывода отелей с фильтром по убыванию цены, по возрастанию цены и по диапозону цены и растоянию от центра

Дата релиза проекта: 20.11.2021

## Стек технологий и библиотек

- python 3.10
- telebot
- Translator
- Requests 
- python-decouple


Чат бот компании **TooEasyTravel**

Ник бота в телеграмме - **@Too_Easy_Travel_GM_BOT**



### Результат проекта

#### Доступные команды:

#### /bestdeal

Файл: botrequests\bestdeal.py

Описание: Вывод подходящих отелей по расположению от центра и цене

#### /highprice

Файл: botrequests\highprice.py

Описание: Вывод самых дорогих отелей города

#### /lowprice

Файл: botrequests\lowprice.py

Описание: Вывод самых дешевых отелей города

#### /history

Файл: botrequests\history.py

Описание: Вывод истории поиска отелей

### Начало работы:

1. Для работы с проектом установите библиотеки из файла requirements.txt (В терминале введите команду `pip install -r requirements.txt`)

2. Затем создайте файл .env и задайте переменные: 

BOT_TOKEN = 'Ваш токен для подключения к telegram'
HEAD = 'Ваш токен для подключения API hotels.com (Будет указан в строке X-RapidAPI-Key раздела botrequests)'

3. Запустите файл main.py
