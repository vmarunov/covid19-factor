import json
import os

from datetime import datetime
from time import sleep

import requests
from dateutil.relativedelta import relativedelta

HOST = 'https://api.covid19api.com'
POPULATION = None
COUNTRIES = None
CONFIRMED = dict()


def to_date(date_str):
    res = datetime.strptime(date_str, '%Y-%m-%d')
    return res.date()


def to_str(date):
    return date.strftime('%Y-%m-%d')


def add_days(date_str, days):
    res = to_date(date_str) + relativedelta(days=days)
    return to_str(res)


def get_countries():
    global COUNTRIES
    if COUNTRIES is None:
        COUNTRIES = requests.get(f'{HOST}/countries').json()
    return COUNTRIES


def get_confirmed(country, date):
    global CONFIRMED
    key = date + ',' + country
    if key not in CONFIRMED:
        try:
            prev_date = add_days(date, -1)
            data = requests.get(
                f'{HOST}/country/{country}/status/confirmed?'
                f'from={prev_date}&to={date}').json()
            CONFIRMED[key] = [
                entry for entry in data
                if entry['Province'] == ''][-1]['Cases']
            sleep(2)
        except:
            print(data)
            sleep(2)
            CONFIRMED[key] = 0
    return CONFIRMED[key]


def calc_factor(slug, country, date, days=14):
    population = get_population(country)
    if not population:
        return country, None, None, None
    confirmed_end = get_confirmed(slug, date)
    confirmed_begin = get_confirmed(slug, add_days(date, -days))
    sicked = confirmed_end - confirmed_begin
    factor = sicked / (population / 100000)
    return country, factor, confirmed_end, sicked


def get_population(country):
    global POPULATION
    if POPULATION is None:
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, 'countries.json')) as fp:
            data = json.load(fp)
        POPULATION = {
            entry['country'].lower(): entry['population']
            for entry in data
        }
    return POPULATION.get(country.lower())


if __name__ == '__main__':

    res = calc_factor('singapore', 'Singapore', '2020-07-24')
    print(res)
