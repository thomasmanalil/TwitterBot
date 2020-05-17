from quickchart import QuickChart



def generate_chart_one_data_set(dates, daily_deaths):
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
                "data": daily_deaths
            }]
        },
        "pointRadius": "0",
        "fill": "False"
    }
    return qc.get_short_url()

# print(qc.get_url())
