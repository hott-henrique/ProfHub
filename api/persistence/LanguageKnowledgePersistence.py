from api.persistence.connector import get_postgres_db


class LanguageKnowledgePersistence(object):

    def create(self, language_knowledge: dict) -> int | None:
        uid = language_knowledge["uid"]
        language = language_knowledge["language"]
        proficiency_level = language_knowledge["proficiency_level"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    INSERT INTO ProfHub.LanguageKnowledge(uid, language, proficiency_level)
                   	VALUES (%s, %s, %s)
                    RETURNING id;
                ''',
                (uid, language, proficiency_level)
            )

            data: dict = cursor.fetchone()

            return data['id'] if data else None

    def update(self, id: int, language_knowledge: dict):
        uid = language_knowledge["uid"]
        language = language_knowledge["language"]
        proficiency_level = language_knowledge["proficiency_level"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    UPDATE ProfHub.LanguageKnowledge AS l
                    SET
                        uid = %s,
                        language = %s,
                        proficiency_level = %s
                    WHERE l.id = %s;
                ''',
                (uid, language, proficiency_level, id)
            )

            return cursor.rowcount != 0

    def delete(self, id: int):
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    DELETE
                    FROM ProfHub.LanguageKnowledge AS l
                    WHERE l.id = %s;
                ''',
                (id, )
            )

            return cursor.rowcount != 0

    def get_all_from_uid(self, uid: int) -> list[dict]:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.LanguageKnowledge AS l
                    WHERE l.uid = %s;
                ''',
                (uid, )
            )

            return cursor.fetchall()

    def search(self, query: str, proficiency_level: str | None = None) -> list[dict]:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.LanguageKnowledge AS l
                    WHERE
                        l.language::TEXT ILIKE %(query)s
                ''',
                { "query": f"%{query}%" }
            )

            data = cursor.fetchall()

            if proficiency_level:
                data = list(filter(lambda obj: obj["proficiency_level"] == proficiency_level, data))

            return data
