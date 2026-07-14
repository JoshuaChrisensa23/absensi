import os
import time
import serial

port = os.environ.get("FINGERPRINT_PORT", "COM3")
ser = serial.Serial(port, 115200, timeout=1)
print(f"Connected -> {port}")

start = time.time()
while time.time() - start < 15:
	line = ser.readline().decode(errors="ignore").strip()
	if line:
		print(f"RAW: {line!r}")

print("Done listening")
