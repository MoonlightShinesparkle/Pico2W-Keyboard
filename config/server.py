import wifi # type: ignore
import socketpool # type: ignore
import microcontroller
import binascii
from adafruit_httpserver import GET, Request, Response, Server, FileResponse, PUT
from keysys.KeyTypes import BaseKey

UID = microcontroller.cpu.uid
DecodedUID = binascii.hexlify(UID).decode("ascii")[-4:]

wifi.radio.start_ap(ssid=f"KeyboardConfig-{DecodedUID}", password="KbdConfig")

Pool = socketpool.SocketPool(wifi.radio)
PicoServer = Server(Pool,"/config")
BindedKeys : list[list[BaseKey]] = []

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

@PicoServer.route("/Update",PUT)
def UpdateRoutine(request : Request):
	return Response(request,"Data uploaded to pico!")

def InitSetup():
	PicoServer.start(str(wifi.radio.ipv4_address_ap),80)
	print("Server started!\nConnect at:")
	print(wifi.radio.ipv4_address_ap)
