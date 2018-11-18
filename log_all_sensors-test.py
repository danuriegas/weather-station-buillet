#!/usr/bin/python3
import interrupt_client, bme680, ds18b20_therm, database
# import wind_direction
import SI1145.SI1145 as SI1145

bme = bme680.BME680(i2c_addr=0x77)  # temp in C, pressure in hPa and humidity in %RH
# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.
bme.set_humidity_oversample(bme680.OS_2X)
bme.set_pressure_oversample(bme680.OS_4X)
bme.set_temperature_oversample(bme680.OS_8X)
bme.set_filter(bme680.FILTER_SIZE_3)

temperature=20
pressure=1000
humidity=90

si = SI1145.SI1145()
vis = 0
IR = 0
uvIndex = 45 / 100.0
temp_probe = 21
#temp_probe = ds18b20_therm.DS18B20()
wind_dir = 0
#wind_dir = wind_direction.wind_direction(adc_channel = 0, config_file="wind_direction.json")
#interrupts = interrupt_client.interrupt_client(port = 49501)
wind =0
gust =0
rain=0
temp=20

db = database.weather_database()  # Local MySQL db
wind_average = 0
#wind_average = wind_dir.get_value(10) #ten seconds

print("Inserting...")
db.insert(temperature, pressure, humidity, temp_probe, vis, IR, uvIndex, wind_average, wind, gust, rain)
print("done")

#interrupts.reset()