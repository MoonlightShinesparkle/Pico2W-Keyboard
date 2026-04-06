import board
import busio
import data.Mem24lc16 as Mem24lc16
from adafruit_hid.keycode import Keycode
import keysys.KeyTypes as KeyTypes

i2c : busio.I2C = busio.I2C(board.GP11,board.GP10)

EEProm : Mem24lc16.Mem24LC16 = Mem24lc16.Mem24LC16(i2c)

# StarryKbdForm in bytes
MAGICNO = [
			   0x53,0x74, # St
			   0x61,0x72, # ar
			   0x72,0x79, # ry
			   0x4B,0x62, # Kb
			   0x64,0x46, # dF
			   0x6F,0x72, # or
			   0x6D       # m
		   ]

# Key press index
KEYIND = 0x01

# Multiple press index
PRESSIND = 0x02

# Text typing index
TEXTIND = 0x03

# Default data
DEFAULTDATA = [
	KEYIND,Keycode.Q,KEYIND,Keycode.W,KEYIND,Keycode.E,KEYIND,Keycode.R,KEYIND,Keycode.T,
	KEYIND,Keycode.Y,KEYIND,Keycode.U,KEYIND,Keycode.I,KEYIND,Keycode.O,KEYIND,Keycode.P,
	KEYIND,Keycode.A,KEYIND,Keycode.S,KEYIND,Keycode.D,KEYIND,Keycode.F,KEYIND,Keycode.G,
	KEYIND,Keycode.H,KEYIND,Keycode.J,KEYIND,Keycode.K,KEYIND,Keycode.L,KEYIND,Keycode.Z,
	KEYIND,Keycode.X,KEYIND,Keycode.C,KEYIND,Keycode.V,KEYIND,Keycode.B,KEYIND,Keycode.N
]

# Determines the file's end point
FILEEND = 0x04

# Print EEPROM length
def PrintLen():
	print(f"Initialized with EEPROM length of {len(EEProm)}")

# Clear EEPROM data
def ClearData():
	for x in range(EEProm.Length):
		EEProm[x] = 0

# Load default data
def LoadDefaults():
	ClearData()
	Ptr : int = 0
	for x in MAGICNO:
		EEProm[Ptr] = x
		Ptr += 1

	for x in DEFAULTDATA:
		EEProm[Ptr] = x
		Ptr += 1
	EEProm[Ptr] = FILEEND

# Reads block data from EEPROM
# Data may be found in the following format:
# [Magic number] -> blocks
# Blocks may be found in the following format:
# 0x01 [ENUM] 			| 2 bytes, second byte is directly loadable
# 0x02 [Size] [N ENUM] 	| Size +2 bytes
# 0x03 [Size] [Text]   	| Size +2 bytes
# 0x04 					| End
def LoadBlocks(Modifiable : list[list[KeyTypes.BaseKey]]):
	Ptr : int = len(MAGICNO)
	XPos : int = 0
	YPos : int = 0

	# Max board X and Y button coords
	MaxY : int = len(Modifiable)
	MaxX : int = len(Modifiable[0])

	while True:
		if (Ptr >= EEProm.Length) or (YPos >= 5):
			break

		BlockType : int = EEProm[Ptr]

		if BlockType == 0x01:
			Data : int = EEProm[Ptr+1]
			Ptr += 2
			# Create normal key and store in array
			Modifiable[YPos][XPos] = KeyTypes.NormalKey(Data)

		elif BlockType == 0x02:
			Size : int = EEProm[Ptr+1]
			Ptr += 2
			Data = []
			# Create multiple keypress key and store in array
			NewKey : KeyTypes.MultipressKey = KeyTypes.MultipressKey()
			
			for x in range(Size):
				Data[x] = EEProm[Ptr]
				Ptr += 1

			NewKey.Data = Data
			Modifiable[YPos][XPos] = NewKey

		elif BlockType == 0x03:
			Size : int = EEProm[Ptr+1]
			Ptr += 2
			Data = ""
			# Create text key and store in array
			NewKey : KeyTypes.TextWriterKey = KeyTypes.TextWriterKey()

			for x in range(Size):
				Data += chr(EEProm[Ptr])
				Ptr += 1

			NewKey.Data = Data
			Modifiable[YPos][XPos] = NewKey


		elif BlockType == 0x04:
			break

		else:
			Ptr += 1

		XPos += 1
		if XPos >= MaxX:
			XPos = 0
			YPos += 1

			if YPos >= MaxY:
				# Data overflow
				break



# Function to preload the needed data for the calc
def Preload(Modifiable : list[list[KeyTypes.BaseKey]]):
	# Checks if it has viable preloaded data
	Loadable : bool = True

	print("Loading data from EEPROM...")

	for x in range(len(MAGICNO)):
		Val : int = MAGICNO[x]
		Stored : int = EEProm[x]
		if (Val != Stored):
			Loadable = False
			break
	
	print("Found viable data!" if Loadable else "Loading default data...")
	if not Loadable:
		LoadDefaults()
		print("Loaded default data")

	LoadBlocks(Modifiable)
