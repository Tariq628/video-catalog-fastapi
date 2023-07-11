# Video Catalog API

This is a simple Video Catalog API built with FastAPI and PostgreSQL. It allows you to perform CRUD (Create, Read, Update, Delete) operations on video resources.

## Prerequisites

Before running the API, make sure you have the following prerequisites installed:

- Python 3.x
- PostgreSQL (with necessary database setup)

## Installation

1. Clone the repository:

```shell
git clone https://github.com/tariq628/video-catalog-fastapi.git
```

Go to the project directory

```bash
  cd video-catalog-fastapi
```

Create a python virtual environement

```bash
  python -m venv venv
```

Start the virtual environement

```bash
  venv\Scripts\activate
```

install required packages

```bash
  pip install -r requirements.txt
```

Start the Server

```bash
  uvicorn video_catalog_api.main:app --reload
```

Run testcases

```bash
  pytest
```

Access the API at 

```bash
  http://127.0.0.1:8000/
```


## API Reference

```http
  POST /videos/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title` | `string` | **Required** title of the video.  |
| `description` | `string` | **Required** description of the video |
| `duration` | `integer` | **Required**. duration of the video |

#### Get single video

```http
  GET /videos/{video_id}
```


#### Edit the video's duration

```http
  PUT /videos/{video_id}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `duration` | `integer` | **Required**. duration of the video |


#### Get vidoes with offset and limit

```http
   GET /videos?limit=1&offset=0
```

## Authors

- [@tariq](https://www.github.com/tariq628)
