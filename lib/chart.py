import json
import logging
from typing import List
from quickchart import QuickChart

logging.basicConfig(level=logging.DEBUG)
border_width = 2
def quickchart(width: int, height: int, dataset: List[float],background_clr:str = "0x000000",line_clr:str = "rgb(255,255,255)",saved_image_path:str=None):
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
                    "backgroundColor": background_clr,
                    "borderColor": line_clr,
                    "borderWidth":border_width,
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
    logging.debug(f"\r\n{qc.get_url()}")

    # Print a short chart URL
    logging.debug(qc.get_short_url())
    # Write a file
    if saved_image_path:
        qc.to_file(saved_image_path)

    # Get image data

    return qc
