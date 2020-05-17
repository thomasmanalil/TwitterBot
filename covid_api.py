
import requests
import os


def get_covid_daily_deaths(country):
    url = "https://api.covid19api.com/dayone/country/"+country
    response = requests.get(url)
    data = response.json()
    return data