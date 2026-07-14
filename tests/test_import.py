try: 
	import cv2
	print("[OK] OpenCV")
except Exception as e:
	print("[Error] OpenCV")
	print(e)

try:
	import face_recognition
	print("[OK] face_recognition")
except Exception as e:
	print("[ERROR] face_recognition")
	print(e)

try:
	from pyfingerprint.pyfingerprint import PyFingerprint
	print("[OK] pyfingerprint")
except Exception as e:
	print("[ERROR] pyfingerprint")
	print(e)

try:
	import sqlite3
	print("[OK] SQLite")
except Exception as e:
	print("[ERROR] SQLite")
	print(e)

print()

print("Import Test Finished")

