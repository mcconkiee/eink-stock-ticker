# ePaper + Pi

## Goal
This is my first go at a display on a raspberry pi. The goal is to display a real time quote of the `VIX` ticker and show the results on an eink display

## Hardware
## Software

### Setup

* clone and cd into source code
* create a virtual env
* install dependencies


```
mkvirtualenv -p python3.9 vix
workon vix
pip install -r requirements.txt
python3 ./drawing.py && open imgs/quote.png
pip uninstall pandas
pip install pandas==1.3.5
```
