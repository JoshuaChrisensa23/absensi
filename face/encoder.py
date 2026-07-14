import os
import pickle

import face_recognition

from .utils import (
	load_face_image,
	encode_face
)

class FaceEncoder:
	def __init__(self):
		self.encodings=[]
		self.names=[]

	def add_image(self, image_path, person_name):
		image=load_face_image(image_path)
		encoding=encode_face(image)

		if encoding is None:
			print(f"[Warning] No Face Found: {image_path}")
			return False
		self.encodings.append(encoding)
		self.names.append(person_name)

		print(f"[OK] {image_path}")
		return True

	def encode_folder(self, samples_folder):
		print("=" * 50)
		print("Encoding Face Dataset")
		print("=" * 50)

		for person in sorted(os.listdir(samples_folder)):
			person_path = os.path.join(samples_folder, person)
			if not os.path.isdir(person_path):
				continue
			print(f"\nPerson:{person}")
			for img in os.listdir(person_path):
				if img.lower().endswith((".jpg",".jpeg",".png")):
					self.add_image(
						os.path.join(person_path, img),
						person
					)
		print("\nEncoding Finished")
		print(f"Total Face: {len(self.encodings)}")

	def save(self,filename):
		data={
			"encodings": self.encodings,
			"names": self.names
		}
		with open(filename, "wb") as f:
			pickle.dump(data, f)
		print(f"\nSaved -> {filename}")

	def load(self,filename):
		with open(filename, "rb") as f:
			data=pickle.load(f)
		self.encodings=data["encodings"]
		self.names=dat["names"]

		print("Encoding Loaded")

	def get_total(self):
		return len(self.encodings)
