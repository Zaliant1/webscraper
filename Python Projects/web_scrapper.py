# from _typeshed import Self
from ctypes import cast
from distutils.log import error, info
from fileinput import filename
from pickle import TRUE
from pydoc import synopsis
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
    find_all = soup.find_all("div", {"data-qa": "cast-crew-item"})

    for a in find_all:
        safe_name = ""
        name = a.find("span", class_="characters subtle smaller").get(
            "title").strip()  # gets the actor

        try:
            safe_name = a.find("a", {"data-qa": "cast-crew-item-img-link"}).get(
                "href", "").replace("/celebrity/", "").strip()
        except:
            safe_name = name

        role = a.find(
            "span", class_="characters subtle smaller").get_text().strip()
        role = convert_unicode_to_ascii(role)

        if role in cast_data:
            role = ", ".join([i.strip().replace(",", "") for i in a.find(
                "span", class_="characters subtle smaller").get_text(
            ).split("\n") if i.strip() != "" and i.strip().lower() != "voice"])

        cast_data[safe_name] = {
            "name": name,
            "role": role,
        }
    return cast_data

# def get_cast(soup):
#     results = soup.find(class_="castSection").find_all(
#         class_="cast-item media")
#     cast = {}

#     for span in results.find_all("span"):
#         actor_name = span.get("title").strip()  # gets the actor
#         if actor_name in cast:

#             role = ", ".join([i.strip().replace(",", "") for i in span.get_text(
#             ).split("\n") if i.strip() != "" and i.strip().lower() != "voice"])
#             role = convert_unicode_to_ascii(role)
#             cast[actor_name] = role

#         else:
#             # sets the value to none on first interation
#             cast[actor_name] = None

#     return cast


# def foobar(soup):
#     cast_data = {}
#     safe_names_soup = soup.find_all("a", {"data-qa": "cast-crew-item-link"})
#     for name, role in get_cast(soup).items():
#         safe_name = None
#         for a in safe_names_soup:
#             if a.span.get("title").strip() == name:
#                 safe_name = a.get("href", "").replace(
#                     "/celebrity/", "").strip()

#         if safe_name:
#             cast_data[safe_name] = {
#                 "name": name,
#                 "role": role,
#             }
#     return cast_data

# getting the movie links


def get_movie_list(soup):
    raw_title_list = []
    title_find = soup.find("search-page-result", slot="movie")
    for i in title_find(slot="title", href=True):
        raw_title_list.append(i['href'])
    return [s.replace("https://www.rottentomatoes.com/m/", "") for s in raw_title_list]

# opening a .json


def json_read(filename):
    with open(filename) as read_file:
        data = json.load(read_file)
    read_file.close()
    return data


# function to write if .json doesn't exist


def movie_json_write(moviefile, data):
    with open(moviefile, "w") as outfile:
        json.dump(data, outfile, indent=2)
    outfile.close()


def cast_json_write(castfile, data):
    with open(castfile, "w") as outfile:
        json.dump(data, outfile, indent=2)
    outfile.close()


# main movie fetch


def fetch_movie_data(movie_title):
    moviefile = f"{MOVIE_DIRECTORY}/{movie_title}.json"

    if os.path.exists(moviefile):
        return json_read(moviefile)
    else:
        time.sleep(0.05)
        URL = f"https://www.rottentomatoes.com/m/{movie_title}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

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
        return movie_data


def fetch_cast_data(cast_member):
    cast_url = cast_member.replace(" ", "_")
    castfile = f"{CAST_DIRECTORY}/{cast_url}.json"

    if os.path.exists(castfile):
        return json_read(castfile)
    else:
        time.sleep(0.05)
        URL = f"https://www.rottentomatoes.com/celebrity/{cast_url}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        cast_data = {
            "name": get_cast_name(soup),
            "safe_name": cast_url,
            "image": get_cast_img(soup),
            "birthday": get_cast_birthday(soup),
            "summary": get_cast_summary(soup),
        }
        cast_json_write(castfile, cast_data)

        return cast_data


def main(search_text):
    URL = f"https://www.rottentomatoes.com/search?search={search_text}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return [fetch_movie_data(title) for title in get_movie_list(soup)]


if __name__ == "__main__":
    search_text = ""
    for title in main(search_text):
        fetch_movie_data(title)
