# **F**astAPI **S**tremlit and **P**ostgreSQL Template

FSP is a project template for using fastapi, streamlit and postgres in containers.

## Running the project

The project will be available at: http://localhost:8080

```bash
$ mkdir -p data/postgres data/upload
$ docker compose up --build -d
```

## Developing the Streamlit App

To develop the streamlit app with hotreloading you need to first build compose, then stop the app container and start the app on the host.

```bash
$ mkdir -p data/postgres data/upload
$ docker compose up --build -d
$ docker stop app
$ export $(grep -v '^#' ./environments/app-dev.env | xargs)
$ streamlit run app/app.py
```

## Developing the API

To develop the api with hotreloading you need to first build compose, then stop the api container and start the api on the host.
**If the streamlit app still running on container it will not connect to the api properly!**

The uvicorn WatchFilesReload will throw some erros but no need to panic, just ignore.

```bash
$ mkdir -p data/postgres data/upload
$ docker compose up --build -d
$ docker stop api
$ export $(grep -v '^#' ./environments/api-dev.env | xargs)
$ fastapi dev api --port 8081
```
