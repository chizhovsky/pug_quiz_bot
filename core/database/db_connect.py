import asyncpg

from config import db_settings, questions_count


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_user_data(self, user_id, user_name, points, category_id):
        category_id = str(category_id)
        query = (
            f"INSERT into users "
            f"(user_id, user_name, points, category_{category_id}) "
            f"VALUES ({user_id}, '{user_name}', {points}, {points}) "
            f"ON CONFLICT (user_id) DO UPDATE SET "
            f"user_name='{user_name}', "
            f"points = users.points + {points}, "
            f"category_{category_id} = users.category_{category_id} + {points}"
        )
        await self.connector.execute(query)


async def connect_to_postgres():
    try:
        conn = await asyncpg.create_pool(
            host=db_settings["host"],
            database=db_settings["name"],
            user=db_settings["user"],
            password=db_settings["password"],
            port=db_settings["port"],
        )
        return conn
    except Exception as error:
        print(error)


async def get_random_questions(category):
    conn = await connect_to_postgres()
    try:
        questions = await conn.fetch(
            f"SELECT * FROM questions WHERE {category} = ANY (category_ids) "
            f"ORDER BY RANDOM() LIMIT {questions_count};"
        )
        return questions
    except Exception as error:
        print("Ошибка получения данных из базы данных:", error)
    finally:
        await conn.close()
