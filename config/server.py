import wifi # type: ignore
import socketpool # type: ignore
import microcontroller
import binascii
from adafruit_httpserver import GET, Request, Response, Server, FileResponse, PUT
from keysys.KeyTypes import BaseKey
from data.Mem24lc16 import Mem24LC16
import data.MemMisc as Misc

UID = microcontroller.cpu.uid
DecodedUID = binascii.hexlify(UID).decode("ascii")[-4:]

wifi.radio.start_ap(ssid=f"KeyboardConfig-{DecodedUID}", password="KbdConfig")

Pool = socketpool.SocketPool(wifi.radio)
PicoServer = Server(Pool,"/config")
BindedKeys : list[list[BaseKey]] = []
MemoryChip : Mem24LC16 = None

def JSONStringify() -> str:
	Returnable : str = "{\"Keys\":["
	for Line in BindedKeys:
		for Key in Line:
			Returnable += Key.JSONParsed+","
	Returnable = Returnable[:-1] + "]}"
	return Returnable

@PicoServer.route("/",GET)
def index(request : Request):
	return FileResponse(request,"index.html","/config")

@PicoServer.route("/Fetch",GET)
def GetKeys(request : Request):
	return Response(request,JSONStringify(),content_type="application/json")

def ClearEEPROM():
	for Index in range(MemoryChip.Length):
		if Index < len(Misc.MAGICNO):
			MemoryChip[Index] = Misc.MAGICNO[Index]
		else:
			MemoryChip[Index] = 0

@PicoServer.route("/Update",PUT)
def UpdateRoutine(request : Request):
	GivenData = request.json()
	print(GivenData)
	KeyDatas : list = GivenData["Keys"]
	MemStart : int = len(Misc.MAGICNO)

	print(f"Data length: {len(KeyDatas)}")

	ClearEEPROM()

	for Index in range(len(KeyDatas)):
		ParsedData : list = []

		KeyType = KeyDatas[Index]["Type"]

		if KeyType == 1:
			ParsedData.append(Misc.KEYIND)
			ParsedData.append(KeyDatas[Index]["Data"])

		elif KeyType == 2:
			ParsedData.append(Misc.PRESSIND)
			GivenData : list = KeyDatas[Index]["Data"]

			DataLen : int = len(GivenData)
			ParsedData.append(DataLen)

			print("Composite key data types:")
			for KeyIndex in range(DataLen):
				print(type(GivenData[KeyIndex]))
				ParsedData.append(int(GivenData[KeyIndex]))

		elif KeyType == 3:
			ParsedData.append(Misc.TEXTIND)
			GivenData : str = KeyDatas[Index]["Data"]

			DataLen : int = len(GivenData)
			ParsedData.append(DataLen)

			for ChrIndex in range(DataLen):
				ParsedData.append(ord(GivenData[ChrIndex]))

		else:
			continue

		print(ParsedData)

		if (MemStart+len(ParsedData)) > (MemoryChip.Length-1):
			print("... breaking?!")
			break

		print("Loading:")
		for EEIndex in range(len(ParsedData)):
			print(ParsedData[EEIndex],end="")
			MemoryChip[MemStart] = ParsedData[EEIndex]
			MemStart += 1

		print()

	MemoryChip[MemStart] = Misc.FILEEND

	return Response(request,"Data uploaded to pico!")

def InitSetup():
	PicoServer.start(str(wifi.radio.ipv4_address_ap),80)
	print("Server started!\nConnect at:")
	print(wifi.radio.ipv4_address_ap)
