import json
from typing import List
from quickchart import QuickChart


def quickchart(width: int, height: int, dataset: List[float]):
    qc = QuickChart()
    qc.width = width
    qc.height = height
    qc.background_color = "transparent"
    qc.version = 3
    qc.device_pixel_ratio = 2.0
    labels = []
    pt = []
    for d in dataset:
        labels.append("")
        pt.append(d)
    # https://www.chartjs.org/docs/latest/samples/line/interpolation.html
    qc.config = {
        "type": 'line',
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "backgroundColor": '0x00000',
                    "borderColor": 'rgb(255, 255, 255)',
                    "borderWidth":1,
                    "data": pt,
                    "fill": False,
                    "radius":0,
                    "cubicInterpolationMode": 'monotone',
                    "tension": 0.4
                }
            ],
        },
        "options": {
            "plugins": {
                "legend": {
                    "display": False,
                }
            },
            "scales": {
                "x": {
                    "display": False,
                },
                "y": {
                    "display": False,
                }
            }
        },
    }

    # Print a chart URL
    # print(qc.get_url())

    # Print a short chart URL
    print(qc.get_short_url())
    # Write a file
    qc.to_file('imgs/chart.png')

    # Get image data

    return qc
