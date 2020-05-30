from quickchart import QuickChart
import logging

def generate_chart_one_data_set(dates, data_set):
    url = None
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)
    try:
        qc = QuickChart()
        qc.width = 500
        qc.height = 300
        qc.device_pixel_ratio = 2.0
        qc.config = {
            "type": "line",
            "data": {
                "labels": dates,
                "datasets": [{
                    "label": "Daily Deaths",
                    "data": data_set
                }]
            },
            "pointRadius": "0",
            "fill": "False"
        }
        url = qc.get_short_url()

    except Exception as ex:
        LOGGER.INFO(ex)
    finally:
        return url
