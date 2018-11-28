# Wiring the weather station HAT

Up to now, we have been testing the sensors connected in a breadboard. For a more robust, long-term installation we will construct a weather station HAT (sensors and connectors attached on top).

Fos assembly the weather station HAT, follow the instructions for this [project](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/11). 
There are some differences between the `build-your-own-weather-station` project and the `weather-station-buillet`, however the assembly of the HAT is the same. The big difference is in software and used digital sensors using the `i2c` interface. We will use the same cables that connect the `BME280` (SDA, SCL, +3V, GND) in the assembly instructions to connect the `Mini RTC Module`, `BME680` and `SI1145` sensors.

Bear in mind that in order to keep the weather station dry, you'll need to separate the raspberry pi HAT from the the `BME680` and `SI1145` sensors, as descibed in the [raspberry pi project](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/12) using the two waterproof enclosures.



