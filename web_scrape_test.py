# from _typeshed import Self
from ctypes import cast
from pydoc import synopsis
import requests
import json
import os
import time
from bs4 import BeautifulSoup
from sys import argv
from os.path import exists
import unicodedata
import web_scrapper

webpage = argv
CAST_DIRECTORY = "data/cast"


def fetch_cast_data(movie_title):
    castfile = f"{CAST_DIRECTORY}/{movie_title}.json"

    json_data = open(castfile)
    jdata = json.load(json_data)

    for key, value in jdata.items():
        members = key

    time.sleep(0.25)
    URL = f"https://www.rottentomatoes.com/celebrity/{members}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    member_info = {members: {
                "title": get_title(soup),
        "safe_title": movie_title,
        "cover": get_cover_img(soup),
        "score": get_tomatometer(soup),
        "audience_score": get_userscore(soup),
            "synopsis": get_synopsis(soup),
            "cast": get_cast(soup),



    }}

    movie_data = {
        "title": get_title(soup),
        "safe_title": movie_title,
        "cover": get_cover_img(soup),
        "score": get_tomatometer(soup),
        "audience_score": get_userscore(soup),
            "synopsis": get_synopsis(soup),
            "cast": get_cast(soup),
    }
    movie_json_write(moviefile, movie_data)

    cast_json_write(castfile, get_cast(soup))
     json_data = open(castfile)
      jdata = json.load(json_data)

       for key, value in jdata.items():
            nested = {key: {
                "title": get_title(soup),
                "safe_title": movie_title,
                "cover": get_cover_img(soup),
                "score": get_tomatometer(soup),
                "audience_score": get_userscore(soup),
                "synopsis": get_synopsis(soup),
                "cast": get_cast(soup),
            }}
            print(nested)

        return movie_data
