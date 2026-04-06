from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Obj with an executable within
# Will hold the data to use
# Has a function for pressing and unpressing

class BaseKey:
	def Press(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None):
		pass

	def Unpress(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None):
		pass

	@property 
	def Weight(self):
		pass

# Normal key press
class NormalKey(BaseKey):
	def __new__(cls, Code : int = None):
		if Code is not None:
			return NormalKey.Create(Code)
		else:
			return super().__new__(cls)

	def Create(Code : int):
		Key : NormalKey = NormalKey()
		Key.Data = Code
		return Key

	Data : int = 0
	def Press(self, Kbd : Keyboard, Layout : KeyboardLayoutUS):
		Kbd.press(self.Data)

	def Unpress(self, Kbd : Keyboard, Layout : KeyboardLayoutUS):
		Kbd.release(self.Data)

	@property
	def Weight(self):
		return 1

# Presses multiple keys at the same time
class MultipressKey(BaseKey):
	Data : list = [0]
	def Press(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None):
		for code in self.Data:
			Kbd.press(code)

	def Unpress(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None):
		for code in self.Data:
			Kbd.release(code)

	@property
	def Weight(self):
		return len(self.Data)

# Writes a whole text
class TextWriterKey(BaseKey):
	Data : str = ""
	def Press(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None):
		Kbd.release_all()
		Layout.write(self.Data,0.05)

	def Unpress(self, Kbd : Keyboard, Layout : KeyboardLayoutUS = None):
		pass

	@property
	def Weight(self):
		return 8