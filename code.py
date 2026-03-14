# General misc
import time

# Modules
import keys
import saving
import config.server

# Delegate key misc to keys module
keys.SetupKeys()

# saving.PrintLen()
# saving.TestWrite()

config.server.InitSetup()

# Constantly scan for key presses
while True:
	keys.ScanRoutine()
	config.server.PicoServer.poll()
	time.sleep(0.00075)