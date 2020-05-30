
import requests
import os


def get_covid_daily_deaths(country="united-kingdom"):
    url = "https://api.covid19api.com/dayone/country/"+country #"https://api.covid19api.com/dayone/country/united-kingdom"
    data = []
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as ex:
        print(ex)
    finally:
        return data