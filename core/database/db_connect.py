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


async def fetch_data():
    conn = await connect_to_postgres()
    try:
        result = await conn.fetch("SELECT * FROM question")
        return result
    except Exception as error:
        print(error)
    finally:
        await conn.close()


async def get_db_questions():
    data = await fetch_data()
    if data:
        for question in data:
            print(question)
    else:
        print("База данных не найдена")
