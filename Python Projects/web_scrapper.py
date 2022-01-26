# from _typeshed import Self
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


# finding title class
def get_title(soup):
  title_find = soup.find(class_="scoreboard__title")
  return title_find.text.strip()
 
# getting the movie image
def get_cover_img(soup):
  cover_find = soup.find("img", class_="posterImage js-lazyLoad")
  if cover_find:
    return cover_find.get("data-src")


# finding scoreboard class
def get_tomatometer(soup):
  tomatometer_find = soup.find(class_="scoreboard")
  return tomatometer_find.get("tomatometerscore")

def convert_unicode_to_ascii(string):
  return unicodedata.normalize('NFKD', string).encode("ascii", 'ignore').decode()

# getting the cast
def get_cast(soup): 
  results = soup.find(class_="castSection")
  cast = {}
 
  for span in results.find_all("span"):
    actor = span.get("title").strip()  # gets the actor
    if actor in cast:
        cast[actor] = ", ".join([i.strip().replace(",", "") for i in span.get_text().split("\n") if i.strip() != "" and i.strip().lower() != "voice"])
        cast[actor] = convert_unicode_to_ascii(cast[actor])
    
    else:
      cast[actor] = None  # sets the value to none on first interation
  
  return cast

# getting the movie links
def get_movie_list(soup):
    raw_title_list = []
    title_find = soup.find("search-page-result", slot="movie")
    for i in title_find(slot="title", href=True):
        raw_title_list.append(i['href'])
    return [s.replace("https://www.rottentomatoes.com/m/", "") for s in raw_title_list]

#opening a .json
def json_read(filename):
  with open(filename) as read_file:
    data = json.load(read_file)  
  read_file.close()
  return data

#function to write if .json doesn't exist
def json_write(filename, data):
  with open(filename, "w") as outfile:
    json.dump(data, outfile, indent=2)
  outfile.close()

def fetch_movie_data(movie_title):
  filename = f"{DATA_DIRECTORY}/{movie_title}.json"
  
  if os.path.exists(filename):
    return json_read(filename)
  
  else:
    time.sleep(0.25)
    URL = f"https://www.rottentomatoes.com/m/{movie_title}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    movie_data = {
      "title": get_title(soup), 
      "cover": get_cover_img(soup), 
      "score": get_tomatometer(soup), 
      "cast": get_cast(soup)
    }
    json_write(filename, movie_data)

    return movie_data


def main(search_text):
  URL = f"https://www.rottentomatoes.com/search?search={search_text}"
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  return [fetch_movie_data(title) for title in get_movie_list(soup)]

if __name__ == "__main__":
  search_text = ""
  for title in main(search_text):
    fetch_movie_data(title)