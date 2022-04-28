# from _typeshed import Self
from ctypes import cast
from distutils.log import error, info
from fileinput import filename
from pickle import TRUE
from pydoc import synopsis
from re import I
from types import NoneType
from matplotlib.font_manager import json_load
from matplotlib.pyplot import get
from pkg_resources import safe_name
import requests
import json
import os
import time
from bs4 import BeautifulSoup
from sys import argv
from os.path import exists
import unicodedata
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


webpage = argv
DATA_DIRECTORY = "data/"
MOVIE_DIRECTORY = "data/movie"
CAST_DIRECTORY = "data/cast"

#
#
#
# cast handling
#
#

# getting the cast name


def get_cast_name(soup):
    cast_name_find = soup.find("h1", {"data-qa": "celebrity-bio-header"})
    if cast_name_find:
        return cast_name_find.text.strip()


# getting the cast image
def get_cast_img(soup):
    base_url = "https://www.rottentomatoes.com"

    cast_img_find = soup.find(
        "img", class_="celebrity-bio__hero-img js-lazyLoad")
    if cast_img_find and "https" in cast_img_find.get("data-src"):
        return cast_img_find.get("data-src")
    elif cast_img_find:
        return base_url + cast_img_find.get("data-src")


# getting the cast birthday
def get_cast_birthday(soup):
    cast_birthday_find = soup.find("p", {"data-qa": "celebrity-bio-bday"})
    if cast_birthday_find:
        return cast_birthday_find.text.strip("Birthday:\n ")


# getting the cast bio
def get_cast_summary(soup):
    cast_summary_find = soup.find("p", {"data-qa": "celebrity-bio-summary"})
    if cast_summary_find:
        return cast_summary_find.text.strip('\n, \\, \t')
#
#
#
# movie handling
#
#
#

# finding title class


def get_title(soup):
    title_find = soup.find(class_="scoreboard__title")
    return title_find.text.strip()


# getting the movie image
def get_cover_img(soup):
    cover_find = soup.find("img", class_="posterImage js-lazyLoad")
    if cover_find:
        return cover_find.get("data-src")
    else:
        return "https://www.rottentomatoes.com/assets/pizza-pie/images/poster_default.c8c896e70c3.gif"


# getting the movie synopsis
def get_synopsis(soup):
    synopsis_find = soup.find(
        "div", class_="movie_synopsis clamp clamp-6 js-clamp")
    return synopsis_find.text.strip()


# getting tomatometer and audience score icons
def get_tomatometer(soup):
    tomatometer_find = soup.find(class_="scoreboard")
    return tomatometer_find.get("tomatometerscore")


def get_userscore(soup):
    userscore_find = soup.find(class_="scoreboard")
    return userscore_find.get("audiencescore")


def convert_unicode_to_ascii(string):
    return unicodedata.normalize('NFKD', string).encode("ascii", 'ignore').decode()


# getting the cast
def get_cast(soup):
    cast_data = {}
    find_all_cast = soup.find_all(
        "div", {"data-qa": "cast-crew-item"})

    for span in find_all_cast:

        name = span.find("span", class_="characters subtle smaller").get(
            "title").strip()  # gets the actor

        # name to None of name is empty
        if name == "":
            name = "No Name"
        else:
            name = name

        # try to get a safe name, if it doesn't exist, set it to Name
        try:
            safe_name = span.find("a", {"data-qa": "cast-crew-item-img-link"}).get(
                "href", "").replace("/celebrity/", "").strip()
        except:
            safe_name = name

        role = span.find(
            "span", class_="characters subtle smaller").get_text().strip()

        if safe_name in cast_data and cast_data[safe_name]["role"] != "":
            cast_data[safe_name]["role"] += f", {role}"
        else:
            cast_data[safe_name] = {
                "name": name,
                "role": role
            }

    return cast_data


# getting the movie links


def get_movie_list(soup):
    raw_title_list = []
    title_find = soup.find("search-page-result", slot="movie")
    for i in title_find(slot="title", href=True):
        raw_title_list.append(i['href'])
    return [s.replace("https://www.rottentomatoes.com/m/", "") for s in raw_title_list]


#
# main movie fetch
#

def fetch_movie_data(movie_title):

    URL = f"https://www.rottentomatoes.com/m/{movie_title}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    movie_data = {
        "title":  get_title(soup),
        "safe_title": movie_title,
        "cover": get_cover_img(soup),
        "score": get_tomatometer(soup),
        "audience_score": get_userscore(soup),
        "synopsis": get_synopsis(soup),
        "cast": get_cast(soup),
    }

    db.collection("Movies").document(movie_title).set(movie_data)
    return movie_data


def fetch_cast_data(cast_member):
    result = db.collection("Cast").document(cast_member).get()

    if result.exists:
        return result.to_dict()
    else:

        URL = f"https://www.rottentomatoes.com/celebrity/{cast_member}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        cast_data = {
            "name": get_cast_name(soup),
            "safe_name": cast_member,
            "image": get_cast_img(soup),
            "birthday": get_cast_birthday(soup),
            "summary": get_cast_summary(soup),
        }

        db.collection("Cast").document(cast_member).set(cast_data)
    return cast_data


def main(search_text):
    URL = f"https://www.rottentomatoes.com/search?search={search_text}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    refs = [db.collection("Movies").document(title)
            for title in get_movie_list(soup)]
    docs = db.get_all(refs)

    output = []
    for i in docs:
        if i.exists:
            output.append(i.to_dict())

        else:
            output.append(fetch_movie_data(i.id))

    return output


def mainceleb(search_text):
    URL = f"https://www.rottentomatoes.com/search?search={search_text}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    celebrity_find = soup.find("search-page-result", slot="celebrity")
    if celebrity_find:
        try:
            return fetch_cast_data(celebrity_find.find("a", {"data-qa": "thumbnail-link"}).get(
                "href", "").replace("/celebrity/", "").strip())
        except:
            return fetch_cast_data(NoneType)


if __name__ == "__main__":
    search_text = ""
    for title in main(search_text):
        fetch_movie_data(title)
