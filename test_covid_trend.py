import unittest
import covid_trend
import covid_api
import chart_api
from unittest.mock import patch
import json
import os
import requests
from requests import ConnectionError, Timeout, HTTPError
from quickchart import QuickChart

def read_json_test_data(json_file_name):
    full_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),f"test-data/{json_file_name}")
    with open(full_file) as json_file:
        json_data=json.load(json_file)
    return json_data

def mock_covid_api_response(country):
    return read_json_test_data("covid_mock_response.json")

def mock_covid_all_provinces(country):
    return read_json_test_data("covid_mock_response__all_province.json")

def mock_covid_empty_json(country):
    return json.loads("[]")

def mock_chart_success(dates, data_set):
    return "http://sample-url"


class CovidTrendTest(unittest.TestCase):
    # TODO: Update Test cases.
    ''' Test cases for get_daily_death_trend '''
    @patch.object(covid_api, 'get_covid_daily_deaths')
    def test_calculate_dataset_no_province(self,mock_covid_api):
        # *valid response with no province
        mock_covid_api.side_effect = mock_covid_api_response
        death_trend = covid_trend.get_daily_death_trend("united-kingdom")
        self.assertEqual(3,len(death_trend[0])) #list dates
        self.assertEqual(3,len(death_trend[1])) #list deaths
        # calculation tests
        daily_deaths = death_trend[1]
        self.assertEqual(10,daily_deaths[0])
        self.assertEqual(-5,daily_deaths[1])
        self.assertEqual(20,daily_deaths[2])


    @patch.object(covid_api, 'get_covid_daily_deaths')
    def test_calculate_dataset_all_province(self, mock_covid_api):
        # * valid response with all provinces
        mock_covid_api.side_effect = mock_covid_all_provinces
        death_trend = covid_trend.get_daily_death_trend("united-kingdom")
        self.assertEqual(0, len(death_trend))

    @patch.object(covid_api, 'get_covid_daily_deaths')
    def test_calculate_dataset_empty_json(self, mock_covid_api):
        # * empty response
        mock_covid_api.side_effect = mock_covid_empty_json
        death_trend = covid_trend.get_daily_death_trend("united-kingdom")
        self.assertEqual(0, len(death_trend))

    @patch.object(requests, 'get')
    def test_get_daily_death_trend_api_timeout_exception(self, mcok_covid_api):
        mcok_covid_api.side_effect = Timeout
        death_trend = covid_trend.get_daily_death_trend("united-kingdom")
        self.assertEqual(0, len(death_trend))

    @patch.object(requests, 'get')
    def test_get_daily_death_trend_api_httperror_exception(self, mcok_covid_api):
        mcok_covid_api.side_effect = HTTPError
        death_trend = covid_trend.get_daily_death_trend("united-kingdom")
        self.assertEqual(0, len(death_trend))

    @patch.object(requests, 'get')
    def test_get_daily_death_trend_api_conectionerror_exception(self, mcok_covid_api):
        mcok_covid_api.side_effect = ConnectionError
        death_trend = covid_trend.get_daily_death_trend("united-kingdom")
        self.assertEqual(0, len(death_trend))

    @patch.object(requests, 'get')
    def test_get_daily_death_trend_api_genericexception_exception(self, mcok_covid_api):
        mcok_covid_api.side_effect = Exception
        death_trend = covid_trend.get_daily_death_trend("united-kingdom")
        self.assertEqual(0, len(death_trend))

    ''' Test casees for get_death_trend_graph'''
    @patch.object(chart_api, 'generate_chart_one_data_set')
    def test_get_death_trend_grapth_success(self, mock_chart):
        mock_chart.side_effect = mock_chart_success
        daily_death_trend = []
        dates = []
        data_set = []
        daily_death_trend.append(dates)
        daily_death_trend.append(data_set)
        chart_url = covid_trend.get_death_trend_graph(daily_death_trend)
        self.assertEqual("http://sample-url", chart_url)

    @patch.object(QuickChart, 'get_short_url')
    def test_get_death_trend_grapth_exception(self, mock_chart):
        mock_chart.side_effect = Exception
        daily_death_trend = []
        dates = []
        data_set = []
        daily_death_trend.append(dates)
        daily_death_trend.append(data_set)
        chart_url = covid_trend.get_death_trend_graph(daily_death_trend)
        self.assertEqual(None, chart_url)


    @patch.object(chart_api, 'generate_chart_one_data_set')
    def test_get_death_trend_grapth_empty_dataset(self, mock_chart):
        mock_chart.side_effect = mock_chart_success
        daily_death_trend = []
        chart_url = covid_trend.get_death_trend_graph(daily_death_trend)
        # when data set is empty, no call to Qucik chart shoud be made
        self.assertEqual(0, mock_chart.call_count)
        # url should  be None
        self.assertEqual(None, chart_url)

    @patch.object(chart_api, 'generate_chart_one_data_set')
    def test_get_death_trend_grapth_invalid_dataset(self, mock_chart):
        mock_chart.side_effect = mock_chart_success
        daily_death_trend = []
        # counts not matching in dates and daily_deaths
        dates = ["date1", "date2"]
        daily_deaths =[2]

        daily_death_trend.append(dates)
        daily_death_trend.append(daily_deaths)

        chart_url = covid_trend.get_death_trend_graph(daily_death_trend)
        # when data set is invalid, no call to Qucik chart shoud be made
        self.assertEqual(0, mock_chart.call_count)
        # url should  be None
        self.assertEqual(None, chart_url)

    ''' Test cases for genereate_covid_trend'''
    def test_genereate_covid_trend_invalid_country(self):
        pass
    def test_genereate_covid_trend_covid_api_exception(self):
        pass
    def test_genereate_covid_trend_chart_api_exception(self):
        pass
    def test_genereate_covid_trend_check_response_string(self):
        pass

    if __name__ == "__main__":
        unittest.main()

