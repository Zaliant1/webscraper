from genericpath import exists
from typing import Tuple
from fastapi import FastAPI
import web_scrapper
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "localhost:3000"
    "127.0.0.1:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/movies/{movie_title}/")
def movie_titles(movie_title: str):
    return web_scrapper.main(movie_title)


@app.get("/movies/{movie_title}/info")
def movie_data_list(movie_title: str):
    return web_scrapper.fetch_movie_data(movie_title)


@app.get("/cast/{cast_member}/info")
def cast_data_list(cast_member: str):
    return web_scrapper.mainceleb(cast_member)


@app.get("/castspecific/{cast_member}/info")
def cast_specific_data(cast_member: str):
    return web_scrapper.fetch_cast_data(cast_member)
