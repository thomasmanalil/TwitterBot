import covid_api
import chart_api
from config import Config
import json
import os

COUNTRIES = None

def load_countries():
    global COUNTRIES
    if (os.path.exists(os.path.join(Config.PARENT_FOLDER,"data/countries.json"))):
        with open(os.path.join(Config.PARENT_FOLDER,"data/countries.json")) as countries_data:
            COUNTRIES = json.load(countries_data)

def get_matching_country(tweet):
    matching_country = None
    tweet_lower = tweet.lower()
    tweet_split_to_words = tweet_lower.split()
    if(COUNTRIES == None):
        load_countries()
    for country in COUNTRIES:
        if(str(country['Country']).lower() in tweet_lower):
            matching_country = country['Slug']
            break
        else:
            if(str(country['Slug']).lower() in tweet_lower):
                matching_country = country['Slug']
                break
            else:
                if(str(country['ISO2']).lower() in tweet_split_to_words):
                    matching_country = country['Slug']
                    break
    return matching_country

def get_daily_death_trend(country):
    # *call Covid19 wrapper and get data
    api_response_json = covid_api.get_covid_daily_deaths(country)
    daily_death_trend =  []
    dates = []
    deaths =  []
    daily_count = []
    # *reading date and deaths from json.
    for data in api_response_json:
        if(data['Province']==''):
            dates.append(data['Date'])
            deaths.append(data['Deaths'])

    # *Calculating daily count
    for i in range(len(deaths)):
        if(i != 0):
            daily_diff = deaths[i] - deaths[i-1]
            daily_count.append(daily_diff)
        else:
            daily_count.append(deaths[i])

    # *adding date and death count to final list.
    if (len(dates) >0 and len(daily_count) >0):
        daily_death_trend.append(dates)
        daily_death_trend.append(daily_count)

    return daily_death_trend

def get_death_trend_graph(daily_death_trend):
    # *call quick chart API wrapper to generate URL
    graph_url = None
    # generate graph only if data set is valid
    if (len(daily_death_trend) == 2 \
        and (len(daily_death_trend[0]) == len(daily_death_trend[1]))):
        # calling QC API
        graph_url = chart_api.generate_chart_one_data_set(dates = daily_death_trend[0], data_set = daily_death_trend[1])
    # graph_url = "http://URL"
    return graph_url

def genereate_covid_death_trend_reply(tweet):
    response_string = None
    try:
        # *Extract contry Id's from tweet content
        country = get_matching_country(tweet)
        if (country == None):
            response_string = "No matching country found."
        else:
            # Get covid data, call covid19 API
            daily_death_trend = get_daily_death_trend(country)
            if (len(daily_death_trend) == 0):
                response_string = "Couldnt find covid data for "+country
            else:
                # *Genereate trend Graph
                url = get_death_trend_graph(daily_death_trend)
                if (url == None):
                    response_string = "Sorry!.Couldn't generate trend for "+country
                else:
                    # *Generate Reply string
                    response_string = "Daily Death Trend for "+country+": " + url
    except Exception as ex:
        Config.LOGGER.info(ex)
    finally:
        return response_string


if __name__ == "__main__":
    print(get_matching_country("United Kingdom"))