import factory
from video_catalog_api.connection_helper import db_connection


class VideoFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Faker("random_int", min=1, max=100000)
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text", max_nb_chars=500)
    duration = factory.Faker("random_int", min=1, max=1000)

    @classmethod
    def create(cls):
        video = super().create()
        connection = db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO videos (id, title, description, duration)
                VALUES (%s, %s, %s, %s)
                """,
                (video["id"], video["title"], video["description"], video["duration"]),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
        return video
