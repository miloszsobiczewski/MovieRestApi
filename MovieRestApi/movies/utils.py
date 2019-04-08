import datetime


def get_date(str_date):
    """

    :param str_date:
    :return:
    """
    date = str_date.split('.')
    (day, mth, year) = [int(x) for x in date]
    date = datetime.date(year, mth, day)
    return date

