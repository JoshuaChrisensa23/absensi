class FingerProtocol:
	@staticmethod
	def parse(message):	
		message = message.strip()
		if message.startswith("MATCH:"):
			return{
				"status": "MATCH",
				"finger_id":int(message.split(":")[1])
			}
		elif message == "NOT_MATCH":
			return{
				"status": "NO_MATCH"
			}
		elif message == "READY":
			return{"status":"READY"}
		return{
			"status":"UNKNOWN",
			"raw": message
		}
