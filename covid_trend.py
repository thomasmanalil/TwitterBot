import covid_api
import chart_api

def get_matching_country(tweet):
    # TODO: update dummy logic
    country = "United-Kingdom"
    return country

def get_daily_death_trend(country):
    # *call Covid19 wrapper and get data
    api_response_json = covid_api.get_get_covid_daily_deaths(country)
    daily_death_trend =  dates = deaths =  daily_count = []
    # *reading date and deaths from json.
    for data in api_response_json:
        if(data['Province']==''):
            dates.append(data['Date'])
            deaths.append(data['Deaths'])
    # *Calculating daily count
    for i in range(len(deaths)):
        if(i != 0):
            daily_count.append(deaths[i] - deaths[i-1])
        else:
            daily_count.append(deaths[i])
    # *adding date and death count to final list.
    daily_death_trend.append(dates)
    daily_death_trend.append(daily_count)
    return daily_death_trend

def get_death_trend_graph(daily_death_trend):
    # TODO: call quick chart API wrapper to generate URL
    graph_url = chart_api.generate_chart_one_data_set(dates = daily_death_trend[0], daily_deaths = daily_death_trend[1])
    # graph_url = "http://URL"
    return graph_url

def genereate_covid_trend(tweet):
    # *Extract contry Id's from tweet content
    country = get_matching_country(tweet)
    # Get covid data, call covid19 API
    daily_death_trend = get_daily_death_trend(country)

    # *Genereate trend Graph
    url = get_death_trend_graph(daily_death_trend)

    # *Generate Reply string
    response_string = "Daily Death Trend for <Country>: " + url
    return response_string

