import datetime


def get_date(str_date):
    date = str_date.split('.')
    (day, mth, year) = [int(x) for x in date]
    date = datetime.date(year, mth, day)
    return date

