import os

import psycopg2
import psycopg2.extras


global G

G = dict()

def get_postgres_db():
    global G

    db = G.get("POSTGRES_DATABASE", None)

    if db is None:
        db = G["POSTGRES_DATABASE"] = psycopg2.connect(
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port="5432",
            dbname=os.environ["POSTGRES_DB"],
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    return db
