import digitalio
import board

def SetupInput(pin : board.Pin, dir : digitalio.Pull = None) -> digitalio.DigitalInOut:
	Port : digitalio.DigitalInOut = digitalio.DigitalInOut(pin)
	Port.direction = digitalio.Direction.INPUT
	if (dir != None):
		Port.pull = dir
	return Port

def SetupOutput(pin : board.Pin, dir : digitalio.Pull = None) -> digitalio.DigitalInOut:
	Port : digitalio.DigitalInOut = digitalio.DigitalInOut(pin)
	Port.direction = digitalio.Direction.OUTPUT
	if (dir != None):
		Port.pull = dir
	return Port