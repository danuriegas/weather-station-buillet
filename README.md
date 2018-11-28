# Weather Station Buillet

This repo contains a modified version of the `Raspberry Pi Oracle Weather Station`.
Follow the guides and tutorials at https://github.com/raspberrypilearning/weather_station_guide (published at www.raspberrypi.org/weather-station) and (https://projects.raspberrypi.org/en/projects/build-your-own-weather-station)

The weather station collects weather data using a variety of sensors. It is designed to be affordable and accurate to be used for private use.

 ## Sensors and measurements
  - A [SI1145](https://www.adafruit.com/product/1777) Digital UV Index / IR / Visible Light sensor.
 - A [BME680](https://www.adafruit.com/product/3660) to measure temperature, pressure, humidity, and indoor air quality.
 - A [DS18B20](https://www.adafruit.com/product/381) digital waterproof thermal probe (with 1m lead)
 - An [anemometer, wind vane and reain gauge](https://www.sparkfun.com/products/8942).


## Hardware
- A Raspberry Pi with WiFi
- Adafruit Perma-Proto HAT for Raspberry Pi Mini Kit - With EEPROM
- Mini RTC Module for Raspberry Pi
- A MCP3008 analogue-to-digital convertor integrated circuit
- Two 4.7 KOhm resistors
- POE Splitter 48V to 5V/2A for Raspberry Pi
- Two SparkFun RJ11 Breakout 
- Two RJ11 6-Pin Connector 
- Weatherproof enclosures; recommended products are this 75x75x37mm box for the BME280 and this larger 150x110x70mm box for the Pi and a soldered HAT
- A breadboard, some jumper wires

## Software

First, you'll need to install the OS Start with a fresh install of the latest version of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/). You can either use the full Desktop version, or the slimmer 'lite' version.

Now, download the necessary files:

    cd ~ && git clone https://github.com/raspberrypi/weather-station

Go to `manual-stup.md` or run the install script to set up the Weather Station software.




