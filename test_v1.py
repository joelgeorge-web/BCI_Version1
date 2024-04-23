import bluetooth


#cidrie car
esp32 = "ESP32test"
address = "A0:A3:B3:AB:89:BA"

devices = bluetooth.discover_devices()

for addr in devices:
    if esp32 == bluetooth.lookup_name(addr):
        address = addr
        break
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((address, port))


while True:
    direction = int(input("Enter direction: "))
    sock.send(str(direction))