# General misc
import time
import digitalio
import board

# USB HID
import usb_hid

# Adafruit HID keyboard misc
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Keyboard and layout init
Kbd = Keyboard(usb_hid.devices)
Layout = KeyboardLayoutUS(Kbd)

# Button 1 misc
button1 = digitalio.DigitalInOut(board.GP0)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.DOWN

x : int = 0

while True:
	if (button1.value):
		Kbd.send(Keycode.M)
		x += 1
		print("Button pressed"+x)
	time.sleep(0.1)