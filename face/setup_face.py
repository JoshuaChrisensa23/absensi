from face.encoder import FaceEncoder

encoder=FaceEncoder()

encoder.encode_folder("face/samples")
encoder.save("face/encodings.pkl")

print()

print("Dataset Ready")
print(f"Total encoding :{encoder.get_total()}")
