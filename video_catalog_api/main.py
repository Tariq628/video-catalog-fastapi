from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import psycopg2

from video_catalog_api.connection_helper import db_connection

app = FastAPI()


class Video(BaseModel):
    title: str
    description: str
    duration: int


def create_video(video: Video):
    # Establish database connection
    connection = db_connection()
    cursor = connection.cursor()

    try:
        # Execute SQL query to insert video into the database
        cursor.execute(
            """
            INSERT INTO videos (title, description, duration)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (video.title, video.description, video.duration),
        )
        video_id = cursor.fetchone()[0]
        connection.commit()
        # Return response with video ID and details
        return {"id": video_id, **video.dict()}
    except psycopg2.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Database error") from e
    finally:
        # Close cursor and database connection
        cursor.close()
        connection.close()


def get_video(video_id: int):
    # Establish database connection
    connection = db_connection()
    cursor = connection.cursor()

    try:
        # Execute SQL query to fetch video by ID
        cursor.execute(
            """
            SELECT * FROM videos WHERE id = %s
            """,
            (video_id,),
        )
        video = cursor.fetchone()

        if video is None:
            raise HTTPException(status_code=404, detail="Video not found")

        # Return video details
        return {
            "id": video[0],
            "title": video[1],
            "description": video[2],
            "duration": video[3],
        }
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Database error") from e
    finally:
        # Close cursor and database connection
        cursor.close()
        connection.close()


def update_video(video_id: int, video: Video):
    # Establish database connection
    connection = db_connection()
    cursor = connection.cursor()

    try:
        # Execute SQL query to update video by ID
        cursor.execute(
            """
            UPDATE videos SET title = %s, description = %s, duration = %s
            WHERE id = %s
            """,
            (video.title, video.description, video.duration, video_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Video not found")

        connection.commit()
        # Return response with video ID and updated details
        return {"id": video_id, **video.dict()}
    except psycopg2.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Database error") from e
    finally:
        # Close cursor and database connection
        cursor.close()
        connection.close()


def delete_video(video_id: int):
    # Establish database connection
    connection = db_connection()
    cursor = connection.cursor()

    try:
        # Execute SQL query to delete video by ID
        cursor.execute(
            """
            DELETE FROM videos WHERE id = %s
            """,
            (video_id,),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Video not found")

        connection.commit()
        # Return response with success message
        return {"message": "Video deleted"}
    except psycopg2.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Database error") from e
    finally:
        # Close cursor and database connection
        cursor.close()
        connection.close()


def get_videos(limit: int = 10, offset: int = 0):
    # Establish database connection
    connection = db_connection()
    cursor = connection.cursor()

    try:
        # Execute SQL query to fetch videos with pagination
        cursor.execute(
            """
            SELECT * FROM videos
            ORDER BY id
            LIMIT %s OFFSET %s
            """,
            (limit, offset),
        )
        videos = []
        for video in cursor.fetchall():
            # Append video details to the list
            videos.append(
                {
                    "id": video[0],
                    "title": video[1],
                    "description": video[2],
                    "duration": video[3],
                }
            )

        # Return the list of videos
        return videos
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Database error") from e
    finally:
        # Close cursor and database connection
        cursor.close()
        connection.close()


@app.post("/videos")
def create_video_endpoint(video: Video):
    return create_video(video)


@app.get("/videos/{video_id}")
def get_video_endpoint(video_id: int):
    return get_video(video_id)


@app.put("/videos/{video_id}")
def update_video_endpoint(video_id: int, video: Video):
    return update_video(video_id, video)


@app.delete("/videos/{video_id}")
def delete_video_endpoint(video_id: int):
    return delete_video(video_id)


@app.get("/videos")
def get_videos_endpoint(limit: int = Query(10, gt=0), offset: int = Query(0, ge=0)):
    return get_videos(limit, offset)
