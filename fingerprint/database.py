import json
import os

class FingerprintDatabase:
	def __init__(self,filename="fingerprint/sample_data.json"):
		self.filename=filename

	def load(self):
		if not os.path.exists(self.filename):
			return[]

		with open(self.filename, "r") as f:
			return json.load(f)

	def save(self, data):
		with open(self.filename, "w") as f:
			json.dump(data, f, indent=4)

	def get_user(self, finger_id):
		users=self.load()
		for user in users:
			if user["finger_id"] == finger_id:
				return user
		return None

	def add_user(self, finger_id, username):
		users =self.load()
		users = [u for u in users if u["finger_id"] != finger_id]
		users.append({
			"finger_id": finger_id,
			"username": username
		})
		self.save(users)

	def remove_by_username(self, username):
		users=self.load()
		remaining=[u for u in users if u["username"] != username]
		removed=len(users) - len(remaining)
		self.save(remaining)
		return removed
