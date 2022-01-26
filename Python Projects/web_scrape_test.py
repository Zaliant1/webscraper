# from _typeshed import Self
import requests
import json
import os
from bs4 import BeautifulSoup
from sys import argv
from os.path import exists
 
webpage = argv
DATA_DIRECTORY = "data/"

# getting the movie links
def get_movie_list(soup):
    raw_title_list = []
    title_find = soup.find("search-page-result", slot="movie")
    for i in title_find(slot="title", href=True):
        raw_title_list.append(i['href'])
    title_list = ([s.replace("https://www.rottentomatoes.com/m/", "") for s in raw_title_list])
    return title_list

def main():
  URL = "https://www.rottentomatoes.com/search?search=jaws"
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  return get_movie_list(soup)

if __name__ == "__main__":
    main()
