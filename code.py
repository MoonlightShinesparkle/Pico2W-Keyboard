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

# Modules
import setup

# Keyboard and layout init
Kbd = Keyboard(usb_hid.devices)
Layout = KeyboardLayoutUS(Kbd)

# Button 1 misc
button1 = setup.SetupInput(board.GP0, digitalio.Pull.DOWN)

# Button 2 misc
button2 = setup.SetupInput(board.GP1, digitalio.Pull.DOWN)

# Button 3 misc
button3 = setup.SetupInput(board.GP2, digitalio.Pull.DOWN)

x : int = 0

while True:
	if (button1.value):
		Kbd.send(Keycode.M)
		x += 1
		print("Button pressed 1 "+str(x))
	if (button2.value):
		Kbd.send(Keycode.O)
		x += 1
		print("Button pressed 2 "+str(x))
	if (button3.value):
		Kbd.send(Keycode.N)
		x += 1
		print("Button pressed 3 "+str(x))
	time.sleep(0.1)