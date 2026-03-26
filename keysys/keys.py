import board
import digitalio
import setup
import time

# Temporal stuffs....
# Adafruit HID keyboard misc
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import usb_hid

Kbd : Keyboard = Keyboard(usb_hid.devices)
Layout : KeyboardLayoutUS = KeyboardLayoutUS(Kbd)

'''
║ *- Inpin & Outpin are keyboard based														   ║
║	   KBD							 Pico													   ║
║	 ╔═════╗						╔════╗													   ║
║	 ╠═════╣			Inpin		║	 ║													   ║
║	 ║	   ║ <┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅ ║	 ║													   ║
║	 ║	   ║ ┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅> ║	 ║													   ║
║	 ╚═════╝			Outpin		╚════╝													   ║
║																							   ║
'''

# Keyboard output pins
KeyboardOutputs = [
	board.GP5, board.GP6, board.GP7, board.GP8, board.GP9
]

# Keyboard input pints
KeyboardInputs = [
	board.GP0, board.GP1, board.GP2, board.GP3, board.GP4
]

# Keyboard LED pins
KeyboardLEDCapsLock = setup.SetupOutput(board.GP12)
KeyboardLEDNumLock = setup.SetupOutput(board.GP13)
KeyboardLEDScrollLock = setup.SetupOutput(board.GP14)

# Loaded pins
KeyboardOutputsLoaded = []
KeyboardInputsLoaded = []

# Key lists
KeysJustPressed = []	# Keys that just got pressed
KeysPressing = []		# Keys that are being pressed
KeyTimeRegistries = []	# How long they have been pressed

# Time registry pressed again
KeySpamDelay = 0.1

# Key press quantity
KeyPressQuantity = 0

# Temporal key array thingy
TempKeys = [
	[Keycode.M,Keycode.O,Keycode.N,Keycode.L,Keycode.I],
	[Keycode.G,Keycode.H,Keycode.T,Keycode.W,Keycode.A],
	[Keycode.S,Keycode.E,Keycode.R,Keycode.SEMICOLON,Keycode.THREE],
	[Keycode.SPACE,Keycode.ENTER,Keycode.LEFT_SHIFT,Keycode.CAPS_LOCK,Keycode.BACKSPACE],
	[Keycode.O,Keycode.U,Keycode.PERIOD,Keycode.EQUALS,Keycode.MINUS]
]

def SetupKeys() -> None:
	"""Prepares keyboard IO pins and stores them into the loaded arrays"""

	global KeysJustPressed
	global KeysPressing
	global KeyTimeRegistries

	KeysJustPressed.clear()
	KeysPressing.clear()
	KeyTimeRegistries.clear()

	for Inpin in KeyboardInputs:
		Pin = setup.SetupOutput(Inpin)
		Pin.value = 1
		KeyboardInputsLoaded.append(Pin)
		KeysJustPressed.append([])
		KeysPressing.append([])
		KeyTimeRegistries.append([])
	
	for Outpin in KeyboardOutputs:
		Pin = setup.SetupInput(Outpin, digitalio.Pull.UP)
		KeyboardOutputsLoaded.append(Pin)
		for Entry in KeyTimeRegistries:
			Entry.append(0)

def ScanRoutine() -> None:
	"""Routine for scanning through all keys"""
	global KeysJustPressed
	global KeysPressing
	global KeyTimeRegistries
	global KeyPressQuantity

	KeyboardLEDCapsLock.value = Kbd.led_on(Kbd.LED_CAPS_LOCK)
	KeyboardLEDNumLock.value = Kbd.led_on(Kbd.LED_NUM_LOCK)
	KeyboardLEDScrollLock.value = Kbd.led_on(Kbd.LED_SCROLL_LOCK)

	# Current matrix pawsitions
	CurrXPos = 0
	CurrYPos = 0

	for y in KeyboardInputsLoaded:
		CurrXPos = 0
		y.value = 0
		time.sleep(0.000015)

		KeysJustPressedEntries : list = KeysJustPressed[CurrYPos]
		KeysPressingEntries : list = KeysPressing[CurrYPos]

		for x in KeyboardOutputsLoaded:
			# Adafruit states max 8 keys pressing at once
			if not x.value and (KeyPressQuantity <= 8):
				# Check if key is in KeysJustPressedEntries list
				if CurrXPos in KeysJustPressedEntries:
					KeysPressingEntries.append(CurrXPos)
					KeysJustPressedEntries.remove(CurrXPos)
					#print("Still pressing "+str(CurrXPos)+", "+str(CurrYPos))

				# Check if key is not in KeysPressingEntries
				elif not (CurrXPos in KeysPressingEntries):
					KeysJustPressedEntries.append(CurrXPos)
					#print("Just pressed "+str(CurrXPos)+", "+str(CurrYPos))
					Kbd.press(TempKeys[CurrYPos][CurrXPos])
					KeyPressQuantity += 1
				# Check if key is in KeysPressingEntries
				else:
					# Continously effectuate action
					pass
			# Check if key is in KeysPressingEntries
			elif CurrXPos in KeysPressingEntries:
				# Remove from KeysPressingEntries
				KeysPressingEntries.remove(CurrXPos)
				Kbd.release(TempKeys[CurrYPos][CurrXPos])
				KeyPressQuantity -= 1
				#print("Released "+str(CurrXPos)+", "+str(CurrYPos))
			
			elif CurrXPos in KeysJustPressedEntries:
				# Remove from KeysJustPressedEntries
				KeysJustPressedEntries.remove(CurrXPos)
				Kbd.release(TempKeys[CurrYPos][CurrXPos])
				KeyPressQuantity -= 1
				#print("Released "+str(CurrXPos)+", "+str(CurrYPos))

			CurrXPos += 1

		y.value = 1
		CurrYPos += 1