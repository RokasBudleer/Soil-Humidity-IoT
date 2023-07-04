# Soil-Humidity-IoT
You will need to change a few lines to set this project up for yourself:

In secrets.py, change the right side of ssid, password, io_username and io_key

In main.py change line 31 & 32
    picowTemp_feed = io.get_feed("TEMPERATURE KEY HERE")
    picowHumid_feed = io.get_feed("HUMIDITY KEY HERE")

If you wish to change the interval of which the microcontroller sends data to your platform, change INTERVAL_L on line 15.
