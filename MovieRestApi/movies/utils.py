import datetime
import requests as r
import json


def get_date(str_date):
    """

    :param str_date:
    :return:
    """
    date = str_date.split('.')
    (day, mth, year) = [int(x) for x in date]
    date = datetime.date(year, mth, day)
    return date


def get_omdb_data(movie_title):
    # read config data
    with open("movies/config.JSON") as config_file:
        conf = json.load(config_file)

    # check for movie in OMDb API
    url = conf['api_url'] % (movie_title, conf['api_key'])
    print(url)
    # check response code
    response = r.get(url)
    data = response.json()
    print(data)
    return data