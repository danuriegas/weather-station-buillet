#!/usr/bin/python3
import json
import time
import math
import os
from gpiozero import MCP3008

class WindDirection(object):
    def __init__(self, adc_channel=0, max_voltage=3.3, config_filename = None):
        self.adc_channel = adc_channel
        self.max_voltage = max_voltage
        self.adc = MCP3008(adc_channel, max_voltage)

        config_path = os.path.join(os.path.dirname(__file__), config_filename)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        
        # read config
        vin = self.config["vin"]
        vdivider = self.config["vdivider"]
        for dir in self.config["directions"]:
            dir["vout"] = self.calc_vout(vdivider, dir["ohms"], vin)
            dir["adc"] = round(dir["vout"] / max_voltage, 3)
        
        sorted_by_adc = sorted(self.config["directions"], key=lambda x: x["adc"])

        for index, dir in enumerate(sorted_by_adc):
            if index > 0:
                below = sorted_by_adc[index - 1]
                delta = (dir["adc"] - below["adc"]) / 2.0
                dir["adcmin"] = dir["adc"] - delta + 1
            else:
                dir["adcmin"] = 1

            if index < (len(sorted_by_adc) - 1):
                above = sorted_by_adc[index + 1]
                delta = (above["adc"] - dir["adc"]) / 2.0
                dir["adcmax"] = dir["adc"] + delta
            else:
                dir["adcmax"] = max_voltage - 1

    def calc_vout(self, r1, r2, vin):
        """
        Ohm's law resistive divider calculation
        """
        return (float(r2) / float(r1 + r2)) * float(vin)
    
    def get_dir(self, adc_value):
        """
        Return the angle in degrees as in config file
        """
        angle = None

        for dir in self.config["directions"]:
            if (adc_value > 0 and
            adc_value >= dir["adcmin"] and
            adc_value <= dir["adcmax"] and
            adc_value < self.max_voltage):
                angle = dir["angle"]
                break

        return angle

    def get_average(self, angles):
        """
        Consider the following three angles as an example: 10, 20, and 30
        degrees. Intuitively, calculating the mean would involve adding these
        three angles together and dividing by 3, in this case indeed resulting
        in a correct mean angle of 20 degrees. By rotating this system
        anticlockwise through 15 degrees the three angles become 355 degrees,
        5 degrees and 15 degrees. The naive mean is now 125 degrees, which is
        the wrong answer, as it should be 5 degrees.
        """

        # http://en.wikipedia.org/wiki/Directional_statistics

        sin_sum = 0.0
        cos_sum = 0.0

        for angle in angles:
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        flen = float(len(angles))
        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average
    
    def get_value(self, time_window=5):
        data = []
        print("Measuring wind direction for %d seconds..." % time_window)
        start_time = time.time()

        while time.time() - start_time <= time_window:
            adc_value = self.adc.read(self.adc_channel)
            direction = self.get_dir(adc_value)
            if direction is not None:  # keep only good measurements
                data.append(direction)
            else:
                print("Could not determine wind direction for ADC reading: %s" % adc_value)

        return self.get_average(data)
    
if __name__ == "__main__":
    obj = WindDirection(adc_channel=0, config_filename="wind_direction.json")
    print(obj.get_value(10))

