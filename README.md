# ePaper + Pi
![quote.png](imgs/quote.png)
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

### Chron
https://crontab.tech/every-10-minutes

eg: every 10 mins
```
*/10 * * * *
```

so

```
chrontab
0 12 * * 1-5 python3 /home/pi/test.py
...exit

chrontab -l
```


# MY PI SETUP

* sudo raspi-config
* Choose Interfacing Options -> SPI -> Yes  to enable SPI interface
* sudo reboot

* add bcm2835 and wiringpi 

```
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz 
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install

```

add source, update numpy and give it dependencies to work with

```

cd /home/pi/vix
pip install -r requirements.txt

pip install --user --upgrade numpy	
sudo apt-get install libatlas-base-dev

```