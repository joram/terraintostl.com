#!/usr/bin/env python

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from payloads import BuildSTLRequest
from worker import add_build_request

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/stl")
async def build_stl(request: BuildSTLRequest) -> dict:
    add_build_request(request)
    return {"hello": "world"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

