import asyncpg

from config import db_settings


async def connect_to_postgres():
    try:
        conn = await asyncpg.connect(
            host=db_settings["host"],
            database=db_settings["name"],
            user=db_settings["user"],
            password=db_settings["password"],
            port=db_settings["port"],
        )
        return conn
    except Exception as error:
        print(error)


async def get_random_questions():
    conn = await connect_to_postgres()
    try:
        questions = await conn.fetch(
            "SELECT * FROM question ORDER BY RANDOM() LIMIT 6"
        )
        return questions
    except Exception as error:
        print("Ошибка получения данных из базы данных:", error)
    finally:
        await conn.close()
