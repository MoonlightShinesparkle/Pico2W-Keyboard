from abc import ABC, abstractmethod

def Nothing():
	pass

# Obj with an executable within
# Will hold the data to use
# Has a function for pressing and unpressing

class BaseKey(ABC):
	@abstractmethod
	def Press():
		pass

	@abstractmethod 
	def Unpress():
		pass

	@property 
	@abstractmethod
	def Weight(self):
		pass

# Normal key press
class NormalKey(BaseKey):
	Data : int = 0
	def Press():
		pass

	def Unpress():
		pass

	@property
	def Weight(self):
		return 1

# Presses multiple keys at the same time
class MultipressKey(BaseKey):
	Data : list = [0]
	def Press():
		pass

	def Unpress():
		pass

	@property
	def Weight(self):
		return len(self.Data)

# Writes a whole text
class TextWriterKey(BaseKey):
	Data : str = ""
	def Press():
		pass

	def Unpress():
		pass

	@property
	def Weight(self):
		return 0