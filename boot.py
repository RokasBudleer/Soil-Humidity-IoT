from secrets import secrets
import ipaddress
import wifi
import socketpool
import board
import digitalio
import time


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# A little flashing of the onboard LED to know that the computer is booting. Remove if unwanted.

led.value = True
time.sleep(0.5)
led.value = False
time.sleep(0.5)
led.value = True
time.sleep(1.5)
led.value = False
time.sleep(1.5)
led.value = True
time.sleep(2.5)
led.value = False
time.sleep(2.5)


#  connect to your SSID
wifi.radio.connect(secrets['ssid'], secrets['password'])

pool = socketpool.SocketPool(wifi.radio)

#   You wont really be able to see these printouts, but provided anyway for troubleshooting. Copy over all contents of boot.py to main.py if needed.
#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

#  pings Google
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))
