import os
import datetime
import requests as r
import json
from MovieRestApi.settings import BASE_DIR


def get_date(str_date):
    """
    Gets date from string format dd.mm.yyyy
    :param str_date:
    :return: datetime.date
    """
    date = str_date.split('.')
    (day, mth, year) = [int(x) for x in date]
    date = datetime.date(year, mth, day)
    return date


def get_omdb_data(movie_title):
    """
    Gets movie details from OMDb API
    :param movie_title:
    :return:
    """
    # read config data
    with open(os.path.join(BASE_DIR, "movies/config.JSON")) as config_file:
        conf = json.load(config_file)

    # check for movie in OMDb API
    url = conf['api_url'] % (movie_title, conf['api_key'])
    # check response code
    response = r.get(url)
    data = response.json()
    return data
