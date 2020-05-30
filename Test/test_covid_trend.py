import unittest
import Bot.covid_trend as covid_trend
import Bot.covid_api as covid_api
import Bot.chart_api as chart_api
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

def mock_death_trend_with_data(country):
    dates = ["20-05-2020", "21-05-2020", "22-05-2020", "23-05-2020", "24-05-2020"]
    daily_count = [5, 10, 12, 20, 40]
    daily_death_trend = []
    daily_death_trend.append(dates)
    daily_death_trend.append(daily_count)
    return daily_death_trend

def mock_get_death_trend_graph(daily_death_trend):
    return "http://sample-url"
class CovidTrendTest(unittest.TestCase):
    def tearDown(self):
        covid_trend.COUNTRIES = None

    def setUp(self):
        covid_trend.COUNTRIES = None

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
    @patch.object(covid_trend, 'get_death_trend_graph')
    @patch.object(covid_trend, 'get_daily_death_trend')
    @patch.object(covid_trend, 'get_matching_country')
    def test_genereate_covid_trend_success(self, mock_country, mock_data_set, mock_chart):
        mock_country.return_value = "united-kingdom"
        mock_data_set.side_effect = mock_death_trend_with_data
        mock_chart.side_effect = mock_get_death_trend_graph
        reply = covid_trend.genereate_covid_death_trend_reply("united-kingdom")
        expected_value = "Daily Death Trend for united-kingdom: http://sample-url"
        self.assertEqual(expected_value, reply)

    @patch.object(covid_trend, 'get_death_trend_graph')
    @patch.object(covid_trend, 'get_daily_death_trend')
    @patch.object(covid_trend, 'get_matching_country')
    def test_generate_covid_trend_no_matching_country(self, mock_country, mock_data_set, mock_chart):
        mock_country.return_value = None
        mock_data_set.side_effect = mock_death_trend_with_data
        mock_chart.side_effect = mock_get_death_trend_graph
        reply = covid_trend.genereate_covid_death_trend_reply("united-kingdom")
        expected_value = "No matching country found."
        self.assertEqual(expected_value, reply)
        self.assertEqual(0, mock_data_set.call_count)
        self.assertEqual(0, mock_chart.call_count)
    @patch.object(covid_trend, 'get_death_trend_graph')
    @patch.object(covid_trend, 'get_daily_death_trend')
    @patch.object(covid_trend, 'get_matching_country')
    def test_genereate_covid_trend_empty_data_set_from_covid_api(self, mock_country, mock_data_set, mock_chart):
        mock_country.return_value = "united-kingdom"
        empty_data = []
        mock_data_set.return_value = empty_data
        mock_chart.side_effect = mock_get_death_trend_graph
        reply = covid_trend.genereate_covid_death_trend_reply("united-kingdom")
        expected_value = "Couldnt find covid data for united-kingdom"
        self.assertEqual(expected_value, reply)
        self.assertEqual(1, mock_country.call_count)
        self.assertEqual(0, mock_chart.call_count)
    @patch.object(covid_trend, 'get_death_trend_graph')
    @patch.object(covid_trend, 'get_daily_death_trend')
    @patch.object(covid_trend, 'get_matching_country')
    def test_genereate_covid_trend_empty_url_from_quick_chart(self, mock_country, mock_data_set, mock_chart):
        mock_country.return_value = "united-kingdom"
        mock_data_set.side_effect = mock_death_trend_with_data
        emtpy_url = None
        mock_chart.return_value = emtpy_url
        reply = covid_trend.genereate_covid_death_trend_reply("united-kingdom")
        expected_value = "Sorry!.Couldn't generate trend for united-kingdom"
        self.assertEqual(expected_value, reply)
        self.assertEqual(1, mock_country.call_count)
        self.assertEqual(1, mock_data_set.call_count)
    def test_genereate_covid_trend_exception_in_getting_death_trend(self):
        pass
    def test_genereate_covid_trend_exception_in_generating_graph(self):
        pass


    # TODO - Add test cases for get_matching_country

    def test_get_matching_country_COUNTRIES_not_loaded(self):
        covid_trend.get_matching_country("sample tweet")
        self.assertIsNot(0, len(covid_trend.COUNTRIES))
    def test_get_matching_country_countries_already_loaded(self):
        countries = [{"Country": "Germany","Slug": "germany","ISO2": "DE"}]
        covid_trend.COUNTRIES = countries
        covid_trend.get_matching_country("sample tweet")
        self.assertEqual(1, len(covid_trend.COUNTRIES))
    def test_get_matching_country_hit_country_full_string_match(self):
        matching_country = covid_trend.get_matching_country("Burkina Faso")
        self.assertEqual("burkina-faso", matching_country)

    def test_get_matching_country_hit_country_as_word_in_tweet(self):
        matching_country = covid_trend.get_matching_country("get Burkina Faso details.")
        self.assertEqual("burkina-faso", matching_country)

    def test_get_matching_country_hit_country_not_as_word_in_tweet(self):
        matching_country = covid_trend.get_matching_country("getBurkina Fasodetails.")
        self.assertEqual("burkina-faso", matching_country)
    def test_get_matching_country_hit_country_at_end_of_tweet(self):
        matching_country = covid_trend.get_matching_country("get Burkina Faso")
        self.assertEqual("burkina-faso", matching_country)

    def test_get_matching_country_hit_slug_full_string_match(self):
        matching_country = covid_trend.get_matching_country("moldova")
        self.assertEqual("moldova", matching_country)
    def test_get_matching_country_hit_slug_as_word_in_tweet(self):
        matching_country = covid_trend.get_matching_country("get moldova data.")
        self.assertEqual("moldova", matching_country)
    def test_get_matching_country_hit_slug_not_as_word_in_tweet(self):
        matching_country = covid_trend.get_matching_country("get moldovadata.")
        self.assertEqual("moldova", matching_country)
    def test_get_matching_country_hit_slug_end_of_tweet(self):
        matching_country = covid_trend.get_matching_country("get trend moldova")
        self.assertEqual("moldova", matching_country)

    def test_get_matching_country_hit_iso2_only_word_in_tweet(self):
        matching_country = covid_trend.get_matching_country("BE")
        self.assertEqual("belgium", matching_country)
    def test_get_matching_country_hit_iso2_small_letter(self):
        matching_country = covid_trend.get_matching_country("be")
        self.assertEqual("belgium", matching_country)
    def test_get_matching_country_hit_iso2_as_word(self):
        matching_country = covid_trend.get_matching_country("get be trend")
        self.assertEqual("belgium", matching_country)
    def test_get_matching_country_hit_iso2_not_as_word(self):
        matching_country = covid_trend.get_matching_country("getBE trend")
        self.assertEqual(None, matching_country)
    def test_get_matching_country_hit_iso2_at_end_of_tweet(self):
        matching_country = covid_trend.get_matching_country("get BE")
        self.assertEqual("belgium", matching_country)
    def test_get_matching_country_hit_iso2_at_start_of_tweet(self):
        matching_country = covid_trend.get_matching_country("BE trend")
        self.assertEqual("belgium", matching_country)
    def test_get_matching_country_no_hit(self):
        matching_country = covid_trend.get_matching_country("BEtrend XYZ")
        self.assertEqual(None, matching_country)
    def test_get_matching_country_partial_match(self):
        matching_country = covid_trend.get_matching_country("trend united")
        self.assertEqual(None, matching_country)
    def test_get_matching_country_multiple_match_iso2(self):
        matching_country = covid_trend.get_matching_country("IN BE")
        self.assertEqual("belgium", matching_country)
    def test_get_matching_country_BLOCK_LETTERS(self):
        matching_country = covid_trend.get_matching_country("BURKINA FASO")
        self.assertEqual("burkina-faso", matching_country)
    def test_get_matching_country_camel_case(self):
        matching_country = covid_trend.get_matching_country("BuRkInA fAsO")
        self.assertEqual("burkina-faso", matching_country)


    if __name__ == "__main__":
        unittest.main()

