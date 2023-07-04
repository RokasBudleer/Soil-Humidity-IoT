import time
from secrets import secrets
import board
import busio
import digitalio
from adafruit_seesaw.seesaw import Seesaw
import ssl
import wifi
import socketpool
import microcontroller
import adafruit_requests
import adafruit_ahtx0
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

INTERVAL_L = 60

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT # set the direction of the pin

aio_username = secrets['io_username']
aio_key = secrets['io_key']

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)
print("connected to io")

try:
# get feed
    picowTemp_feed = io.get_feed("TEMPERATURE KEY HERE")
    picowHumid_feed = io.get_feed("HUMIDITY KEY HERE")
    print("connected to feeds")
except AdafruitIO_RequestError:
    print("Could not get feed from AIO") # If you get this output in your terminal one or both of the keys are wrong.

#   pack feed names into an array for the loop
feed_names = [picowTemp_feed, picowHumid_feed]

#   Tells the computer what connectors to read data from. 
#   If you have changed the wiring from the ones given in the tutorial circuit schema, you will need to change scl and sda.
i2c = busio.I2C(scl=board.GP5, sda=board.GP4, frequency=400000)
ss = Seesaw(i2c, addr=0x36)
print()
print("Sensor test start")
led.value = True # turn the LED on
time.sleep(1) # wait for 1 seconds
    
# read moisture level through capacitive touch pad
touch = ss.moisture_read()
    
# read temperature from the temperature sensor
temp = ss.get_temp()

print("Temperature: " + str(temp) + " degrees Celsius, Humidity: " + str(touch))
print("Test Done.")

led.value = False # turn the LED off
time.sleep(5) # wait for 5 seconds

print()
print("Starting infinite loop...")
while True:
    try:
            #  read sensor
            data = [ss.get_temp(), ss.moisture_read()]
            #  send sensor data to respective feeds
            led.value = True
            for z in range(2):
                io.send_data(feed_names[z]["key"], data[z])
                print("%s %0.1f " % (feed_names[z]["key"], data[z]))
                time.sleep(1)
            #  print sensor data to the REPL
            print()
            led.value = False
            time.sleep(2)
            
    except Exception as e:
        print("Error:\n", str(e))
        #print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        #microcontroller.reset()