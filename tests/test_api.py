from fastapi.testclient import TestClient
from tests.test_data_factory import VideoFactory

from video_catalog_api.main import app

client = TestClient(app)


def test_create_video():
    video_data = VideoFactory.build()
    response = client.post("/videos", json=video_data)
    assert response.status_code == 200
    assert response.json()["title"] == video_data["title"]
    assert response.json()["description"] == video_data["description"]
    assert response.json()["duration"] == video_data["duration"]


def test_get_video():
    test_video = VideoFactory.create()
    video_id = test_video["id"]
    response = client.get(f"/videos/{video_id}")
    assert response.status_code == 200


def test_update_video():
    test_video = VideoFactory.create()
    video_id = test_video["id"]
    updated_video_data = VideoFactory.build()
    response = client.get(f"/videos/")
    response = client.put(f"/videos/{video_id}", json=updated_video_data)
    assert response.status_code == 200
    assert response.json()["id"] == video_id
    assert response.json()["title"] == updated_video_data["title"]
    assert response.json()["description"] == updated_video_data["description"]
    assert response.json()["duration"] == updated_video_data["duration"]


def test_delete_video():
    test_video = VideoFactory.create()
    video_id = test_video["id"]
    response = client.delete(f"/videos/{video_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Video deleted"
