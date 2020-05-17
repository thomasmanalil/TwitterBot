import unittest

class CovidTrendTest(unittest.TestCase):

    ''' Test cases for get_daily_death_trend '''
    def test_get_daily_death_trend_calculation(self):
        pass
    def test_get_daily_death_trend_invalid_country(self):
        pass
    def test_get_daily_death_trend_empty_response_json(self):
        pass
    def test_get_daily_death_trend_api_exception(self):
        pass

    ''' Test casees for get_death_trend_graph'''
    def get_death_trend_grapth_empty_list(self):
        pass
    def get_death_trend_grapth_only_date_range(self):
        pass
    def get_death_trend_grapth_only_dataset(self):
        pass

    ''' Test cases for genereate_covid_trend'''
    def genereate_covid_trend_invalid_country(self):
        pass
    def genereate_covid_trend_covid_api_exception(self):
        pass
    def genereate_covid_trend_chart_api_exception(self):
        pass
    def genereate_covid_trend_check_response_string(self):
        pass