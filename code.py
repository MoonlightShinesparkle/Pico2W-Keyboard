# General misc
import time

# Modules
import keysys.keys as keys
import data.MemInterfacing as MemInterfacing
import config.server as Server

# Delegate key misc to keys module
keys.SetupKeys()

Server.BindedKeys = keys.TempKeys

MemInterfacing.PrintLen()
MemInterfacing.Preload(keys.TempKeys)

Server.InitSetup()

# Constantly scan for key presses
while True:
	keys.ScanRoutine()
	Server.PicoServer.poll()
	time.sleep(0.00075)