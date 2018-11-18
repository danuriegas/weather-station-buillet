#!/usr/bin/python3
import ds18b20_therm

print("""Display Soil Temperature
Press Ctrl+C to exit
""")

temp_probe = ds18b20_therm.DS18B20()

print('Polling:')
try:
    while True:
        if temp_probe.read_temp():
            output = '{0:.2f} C'.format(temp_probe.read_temp())
            print(output)

except KeyboardInterrupt:
    pass