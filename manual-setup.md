# Setting up the Weather Station Buillet software manually.

This document is based on the manual instructions for the [Raspberry Pi weather station](https://github.com/raspberrypilearning/weather-station-guide). 
It has been modified and adapted to the `Weather-Station-Buillet` project.

## Manual installation

1.  Start with a fresh install of the latest version of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/). You can either use the full Desktop version, or the slimmer 'lite' version.

1. Headless Raspberry Pi Setup: Enable SSH by placing a file named “ssh” (without any extension) onto the boot partition of the SD card.

1.  When booting for the first time, you will be presented with the desktop (or a login prompt if you're using the 'lite' version). The default credentials for user _pi_ password _raspberry_.  

1.  If you're using the Desktop version, from the Menu button in the top left-hand corner choose `Preferences` > `Raspberry Pi Configuration`. Otherwise log in and type

```bash
sudo raspi-config
```

1. We recommend that you **change your password**.

1. In the Interfaces tab, enable I2C.

1. A reboot dialogue will appear. Select Yes.

## Setting up the real-time clock

We'll be doing most of the work from the command line. If you're using the Desktop version, open a terminal window using the icon on the menu bar or by pressing `ctrl`+`alt`+`t`.

You'll now be at a prompt:

```bash
pi@raspberrypi: ~ $
```

You can type the commands which follow into this prompt.

First, you'll need to download the necessary files:

```bash
cd ~ && git clone https://github.com/danuriegas/weather-station-buillet
```

We've included an install script to set up the real-time clock automatically. You can run this file or, alternatively, follow the instructions below to set up the RTC manually. We recommend using the install script!

## Setting up the real-time clock

First, you want to make sure you have all the latest updates for your Raspberry Pi:

```bash
sudo apt-get update && sudo apt-get upgrade
```
This section is based on this [tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi). The RTC module must be loaded by the kernel by running:

```bash
sudo modprobe rtc-ds1307
```

You now need to make some changes to a file to allow the Raspberry Pi to use the real-time clock using `i2c` communication with the address `0x68`. You'll need to be running as the super user; type in:

```bash
sudo bash
```

and then, if you have a Rev.2 Raspberry Pi or later:

    echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device

Or if you have the older Rev.1 Raspberry Pi, use:

    echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-0/new_device

Type `exit` to stop being the 'root' user.

Now check the time on the RTC device using:

```bash
sudo hwclock -r
```

## Initialise the RTC with the correct time

Use the `date` command to check that the current system time is correct. If it's correct, then you can set the RTC time from the system clock with the following command:

```bash
sudo hwclock -w
```

If not, you can set the RTC time manually using the command below (you'll need to change the `--date` parameter, as this example will set the date to the 1st of January 2014 at midnight):

```bash
sudo hwclock --set --date="yyyy-mm-dd hh:mm:ss" --utc
```

For example:

```bash
sudo hwclock --set --date="2015-08-24 18:32:00" --utc
```

Then set the system clock from the RTC time:

```bash
sudo hwclock -s
```

Now you need to enable setting the system clock automatically at boot time. You will need to add the RTC kernel module to the file `/etc/modules` so it is loaded when the Raspberry Pi boots. Type the following in the terminal:

```bash
sudo nano /etc/modules
```

Add `rtc-ds1307` at the end of the file.

Next you will need to add the DS1307 device creation at boot by editing the `/etc/rc.local` file by running:

```bash
sudo nano /etc/rc.local
```

and add the following lines to the file:
```bash
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
sudo hwclock -s
date
```

Just before the `exit 0`. Note: If you have a Rev 1 Raspberry Pi, replace `i2c-1` by `i2c-0` above.

To test this out, shutdown your Raspberry Pi, unplug any ethernet cable or wifi dongle and then turn the Raspberry Pi back on. Use the following command in a terminal window to check the date is still set:

    date

Now, the next time you reboot your Raspberry Pi it will read the time from the Real Time Clock.

## Testing the sensors (Pending)

### Install the necessary software packages

Power up your Raspberry Pi and log in. At the command line, type the following:

```bash
sudo apt-get install i2c-tools python-smbus telnet -y
```

Test that the I2C devices are online and working:

```bash
sudo i2cdetect -y 1
```

You should see output similar to this:

```
	 0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- UU 69 6a -- -- -- -- --
70: -- -- -- -- -- -- -- 77                         
```

- `40` = HTU21D, the humidity and temperature sensor.
- `77` = BMP180, the barometric pressure sensor.
- `68` = PCF8523, the real-time clock. It will show as `UU` because it's reserved by the driver.
- `69` = MCP3427, the analogue-to-digital converter on the main board.
- `6a` = MCP3427, the analogue-to-digital converter on the snap-off AIR board.

Note: `40`, `77` and `6a` will only show if you have connected the **AIR** board to the main board.

Now that the sensors are working, we need a database to store the data they produce.

## Database setup

Now you'll set up your Weather Station to automatically log the collected weather data. The data is stored on the Pi's SD card using a database system called MariaDB. Once your station is successfully logging data locally, you'll also be able to [upload that data](oracle.md) to a central Oracle Apex database to share it with others.

### Install the necessary software packages

At the command line, type the following:

```bash
sudo apt-get install -y mariadb-server mariadb-client libmariadbclient-dev
sudo pip3 install mysqlclient
```

If you make a mistake, use the cursor UP arrow to go back to previous lines for editing.

Please note that this will take some time.

### Create a local database within MariaDB

Enter the following:

```bash
sudo mysql
```

You will now be at the MariaDB prompt `MariaDB [(none)]>`. First, create a local database account for the Pi user and assign the necessary privileges. You should also choose a password for this account.

```mysql
create user pi IDENTIFIED by 'password';
grant all privileges on *.* to 'pi' with grant option;
```

Then, create the database:

```mysql
CREATE DATABASE weather;
```

You should now see `Query OK, 1 row affected (0.00 sec)`.

Switch to that database:

```mysql
USE weather;
```

You should see `Database changed`, and your prompt should now be `MariaDB [(weather)]>`.

If MariaDB doesn't do anything when it should, you've probably forgotten the final `;`. Just type it in when prompted and press Enter.

### Create a table to store the weather data

Type the code below, taking note of the following tips:

- Don't forget the commas at the end of the row
- Use the cursor UP arrow to copy and edit a previous line, as many are similar
- Type the code carefully and **exactly** as written, otherwise things will break later
- Use CAPS LOCK!

```
  CREATE TABLE WEATHER_MEASUREMENT(
   ID BIGINT NOT NULL AUTO_INCREMENT,
   REMOTE_ID BIGINT,
   AMBIENT_TEMPERATURE DECIMAL(6,2) NOT NULL,
   BAROMETRIC_PRESSURE DECIMAL(6,2) NOT NULL,
   HUMIDITY DECIMAL(6,2) NOT NULL,
   GROUND_TEMPERATURE DECIMAL(6,2) NOT NULL,
   VIS_LIGHT DECIMAL(6,2) NOT NULL,
   IR_LIGHT DECIMAL(6,2) NOT NULL,
   UV_INDEX DECIMAL(6,2) NOT NULL,
   WIND_DIRECTION DECIMAL(6,2) NULL,
   WIND_SPEED DECIMAL(6,2) NOT NULL,
   WIND_GUST_SPEED DECIMAL(6,2) NOT NULL,
   RAINFALL DECIMAL (6,2) NOT NULL,
   CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY ( ID )
);
```

You should now see `Query OK, 0 rows affected (0.05 sec)`.

Press `Ctrl`+`D` or type `exit` to quit MariaDB.

## Set up the sensor software

We will install the python libraries (if needed) for the different sensors, starting with the [BME680](https://www.adafruit.com/product/3660) - Temperature, Humidity, Pressure and Gas Sensor,   type in:

    sudo pip3 install bme680

Now, we will install the python library for accessing the [SI1145](https://www.adafruit.com/product/1777) temperature sensor written by Joe Gutting, type in:

    pip3 install git+https://github.com/THP-JOE/Python_SI1145

## Start the Weather Station daemon and test it

A daemon is a process that runs in the background. To start the daemon we need for the Weather Station, use the following command:

```bash
sudo ~/weather-station/interrupt_daemon.py start
```

You should see something like `PID: 2345` (your number will be different).

A continually running process is required to monitor the rain gauge and the anemometer. These are reed switch sensors, and the code uses interrupt detection. These interrupts can occur at any time, as opposed to the timed measurements of the other sensors. You can use the **telnet** program to test or monitor the daemon, with the following command:

```bash
telnet localhost 49501
```

You should see something like this:

```
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
OK
```

The following text commands can be used:

- `RAIN`: displays rainfall in ml
- `WIND`: displays average wind speed in kph
- `GUST`: displays wind gust speed in kph
- `RESET`: resets the rain gauge and anemometer interrupt counts to zero
- `BYE`: quits

Use the `BYE` command to quit.

### Set the Weather Station daemon to automatically start at boot

Use the following command to automate the daemon:

```bash
sudo nano /etc/rc.local
```

Insert the following lines before `exit 0` at the bottom of the file:

```bash
echo "Starting Weather Station daemon..."

/home/pi/weather-station/interrupt_daemon.py start
```

Press `Ctrl`+`O` then `Enter` to save, and `Ctrl`+`X` to quit nano.

### Update the MySQL credentials file

You'll need to use the password for the MySQL root user that you chose during installation. If you are **not** in the `weather-station` folder, type:

```bash
cd ~/weather-station
```

then:

```bash
nano credentials.mysql
```

Change the password field to the password you chose during installation of MySQL. The double quotes `"` enclosing the values are important, so take care not to remove them by mistake.

Press `Ctrl`+`O` then Enter to save, and `Ctrl`+`X` to quit nano.

## Automate updating of the database

The main entry points for the code are `log_all_sensors.py`. These will be called by a scheduling tool called [cron](http://en.wikipedia.org/wiki/Cron) to take measurements automatically. The measurements will be saved in the local MySQL database.

You should enable cron to start taking measurements automatically. This is also known as **data logging mode**:

```bash
crontab < crontab.save
```

Your Weather Station is now live and recording data at timed intervals.

You can disable data logging mode at any time by removing the crontab with the command below:

```bash
crontab -r
```

To enable data logging mode again, use the command below:

```bash
crontab < ~/weather-station/crontab.save
```

Please note that you should not have data logging mode enabled while you're working through the lessons in the [scheme of work](https://github.com/raspberrypilearning/weather-station-sow).

### Manually trigger a measurement

You can manually cause a measurement to be taken at any time with the following command:

```bash
sudo ~/weather-station/log_all_sensors.py
```

Don't worry if you see `Warning: Data truncated for column X at row 1` – this is expected.


### View the data in the database

Enter the following command:

```bash
mysql -u root -p
```

Enter the password (the default for the disk image installation is `tiger`). Then switch to the `weather` database:

```bash
USE weather;
```

Run a select query to return the contents of the `WEATHER_MEASUREMENT` table:

```bash
SELECT * FROM WEATHER_MEASUREMENT;
```

![](images/database.png)

After a lot of measurements have been recorded, it will be sensible to use the SQL `where` clause to only select records that were created after a specific date and time:

```bash
SELECT * FROM WEATHER_MEASUREMENT WHERE CREATED > '2018-01-01 12:00:00';
```

Press `Ctrl`+`D` or type `exit` to quit MySQL.

