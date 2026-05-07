from adafruit_hid.keycode import Keycode

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