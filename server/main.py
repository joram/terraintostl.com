#!/usr/bin/env python
import json
import os
import pprint

import requests
import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google.auth.transport import requests
from google.oauth2 import id_token
from starlette.background import BackgroundTasks
from starlette.staticfiles import StaticFiles

from payloads import BuildSTLRequest
from search import get_peak_index
from sessions import save_session, get_session
from worker import get_progress, get_api_url
from worker import build_stl as build_stl_func

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/stl")
async def build_stl(
    request: BuildSTLRequest, background_tasks: BackgroundTasks
) -> dict:
    background_tasks.add_task(build_stl_func, request)
    return {"hello": "world"}


@app.get("/search")
async def search(request: Request) -> dict:
    query = request.query_params.get("query")
    if query is None:
        return {"error": "missing query parameter"}

    print(f"searching for '{query}'")
    results = get_peak_index().search(query)
    return {"results": results}


@app.post("/login")
async def post_login(data: dict) -> dict:
    credential_data = data
    audience = credential_data["clientId"]
    id_info = id_token.verify_oauth2_token(
        credential_data["credential"], requests.Request(), audience
    )

    save_session(
        session_key=id_info["sub"],
        session={
            "name": id_info["name"],
            "email": id_info["email"],
            "picture": id_info["picture"],
        },
    )

    return {
        "session_key": id_info["sub"],
        "name": id_info["name"],
        "email": id_info["email"],
        "picture": id_info["picture"],
    }


@app.get("/stls")
async def get_stls(request: Request) -> dict:
    session_key = request.headers.get("session_key")

    session = get_session(session_key)
    if session is None:
        return {
            "error": f"invalid session_id '{session_key}'",
            "stls": [],
            "in_progress": get_progress(),
        }

    stls = []
    email = session["email"]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    stl_dir = os.path.realpath(f"{dir_path}/../stls/{email}")
    if not os.path.exists(stl_dir):
        os.mkdir(stl_dir)
    filenames = os.listdir(stl_dir)

    filenames.sort()
    for filename in filenames:
        if filename.endswith(".stl"):
            stls.append(
                {
                    "name": filename,
                    "triangles": 69,
                    "filesize": os.path.getsize(
                        os.path.join(f"{dir_path}/../stls/{email}/", filename)
                    ),
                    "status": "done",
                    "url": f"{get_api_url()}/static/{email}/{filename}",
                }
            )
    return {
        "stls": stls,
        "in_progress": get_progress(),
    }


app.mount("/static", StaticFiles(directory="../stls/"), name="stls")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
