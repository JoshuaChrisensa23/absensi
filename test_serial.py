import serial

PORT="/dev/ttyUSB0"
BAUD=115200

ser=serial.Serial(PORT, BAUD, timeout=1)
print("Connected")

while True:
	line=ser.readline().decode(errors="ignore").strip()

	if line:
		print(line)
