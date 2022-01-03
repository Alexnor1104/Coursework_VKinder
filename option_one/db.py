import sqlalchemy
import psycopg2
from config import host, user, password, db_name

try:
    # Подключение к базе данных:

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # проверяем версию сервера PostgreSQL (тест подключения):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )

        print(f"Server version: {cursor.fetchone()}")


except Exception as _ex:
    print("[INFO] Ошибка при работе с PostgreSQL", _ex)

    # Создание новой таблицы (запустить функцию):


def create_table():
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE users(
                id serial PRIMARY KEY,
                id_user varchar(30) NOT NULL,
                first_name varchar(50) NOT NULL,
                link varchar(255) NOT NULL
                );"""
        )

        print("[INFO] Таблица успешно создана")


# вставка данных в таблицу:
def insert_users(id_user, first_name, link):
    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO users (id_user, first_name, link) VALUES('{id_user}', '{first_name}', '{link}');"
        )

        print("[INFO] Данные были успешно добавлены в таблицу!")


def read_users_id():
    # Чтение id_user из таблицы:
    list_ids = []
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id_user FROM users;"
        )
        for i in cursor.fetchall():
            ids = int(i[0])
            list_ids.append(ids)

        return list_ids

