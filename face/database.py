import json
import os

class FaceDatabase:
	def __init__(self,db_file="face/users.json"):
		self.db_file=db_file
		if not os.path.exists(db_file):
			with open(db_file, "w") as f:
				json.dump([], f)
	def load(self):
		with open(self.db_file, "r") as f:
			return json.load(f)

	def save(self,data):
		with open(self.db_file, "w") as f:
			json.dump(data,f,indent=4)

	def add_user(self,username,finger_id):
		users=self.load()
		users.append({
			"username": username,
			"finger_id": finger_id
		})

		self.save(users)

	def find_by_finger(self,finger_id):
		users=self.load()
		for user in users:
			if user["finger_id"] == finger_id:
				return user
		return None
