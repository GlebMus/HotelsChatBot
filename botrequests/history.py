from settings import *
import sqlite3


"""
history_add - функция добавляет данные запроса в базу данных
Параметры:
comm - название команды
comm_time - время и дата вызова команды
comm_result - результат вывода команды
База данных - файл history.bd 
"""


def history_add(user_id: int, city: str, comm: str, comm_time: str, comm_result: str) -> None:
    with sqlite3.connect('history.db') as db:
        try:
            cursor = db.cursor()
            query = """CREATE TABLE IF NOT EXISTS history( user_id INTEGER, city STR, command STR, date STR, 
            hotels STR) """
            cursor.execute(query)
            query2 = "INSERT INTO history (user_id, city, command, date, hotels) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query2, (user_id, city, comm, comm_time, comm_result))
            db.commit()
        except Exception as exp:
            logger.debug(f'Ошибка подключения в файле history.py!(Функция history_add) (debug) \nОшибка:\n{exp}')
            raise


"""
history_command - функция выводит все данные из базы данных и соединяет в строку
База данных - файл history.bd 
Возвращает соединенную строку
"""


def history_command(user_id: int) -> str:
    with sqlite3.connect('history.db') as db:
        try:
            cursor = db.cursor()
            query = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='history'"
            cursor.execute(query)
            results = cursor.fetchall()[0][0]
            if results == 0:
                return 'История поиска пуста!'
            else:
                query2 = f""" SELECT * FROM history WHERE user_id = {user_id}"""
                cursor.execute(query2)
                final_history = ''
                for line in cursor:
                    final_history += f'Команда: {line[2]}\nГород поиска: {line[1]}\nДата ввода команды: {line[3]}\nРезультат поиска:\n{line[4]}\n'
                return final_history
        except Exception as exp:
            logger.debug(f'Ошибка подключения в файле history.py!(Функция history_command) (debug) \nОшибка:\n{exp}')
            raise

