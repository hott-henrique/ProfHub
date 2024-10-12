import os

import fastapi

import psycopg2
import psycopg2.extras


api = fastapi.FastAPI(title="ProfHub - API",
                      root_path="/api",
                      version="0.1.0")

@api.get("/hello")
def hello(user: str = "World") -> str:
    conn =  psycopg2.connect(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port="5432",
        dbname=os.environ["POSTGRES_DB"],
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cursor = conn.cursor()

    cursor.execute("SELECT 1 AS ok;")

    result : dict = cursor.fetchone()

    conn.close()

    return f"Hello, {user}! Is database on? {result['ok'] == 1}"
