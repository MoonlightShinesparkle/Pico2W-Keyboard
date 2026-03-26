import board
import busio
import data.Mem24lc16 as Mem24lc16
from adafruit_hid.keycode import Keycode

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
	0x01,Keycode.Q,0x01,Keycode.W,0x01,Keycode.E,0x01,Keycode.R,0x01,Keycode.T,
	0x01,Keycode.Y,0x01,Keycode.U,0x01,Keycode.I,0x01,Keycode.O,0x01,Keycode.P,
	0x01,Keycode.A,0x01,Keycode.S,0x01,Keycode.D,0x01,Keycode.F,0x01,Keycode.G,
	0x01,Keycode.H,0x01,Keycode.J,0x01,Keycode.K,0x01,Keycode.L,0x01,Keycode.Z,
	0x01,Keycode.X,0x01,Keycode.C,0x01,Keycode.V,0x01,Keycode.B,0x01,Keycode.N
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
def LoadBlocks():
	Ptr : int = len(MAGICNO)
	while True:
		if (Ptr >= EEProm.Length):
			break

		BlockType : int = EEProm[Ptr]
		if Ptr == 0x01:
			pass
		elif Ptr == 0x02:
			pass
		elif Ptr == 0x03:
			pass
		elif Ptr == 0x04:
			break



# Function to preload the needed data for the calc
def Preload():
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
