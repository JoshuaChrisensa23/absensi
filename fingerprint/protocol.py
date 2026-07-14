class FingerProtocol:
	@staticmethod
	def parse(message):	
		message = message.strip()
		if message.startswith("MATCH:"):
			return{
				"status": "MATCH",
				"finger_id":int(message.split(":")[1])
			}
		elif message == "NO_MATCH":
			return{
				"status": "NO_MATCH"
			}
		elif message == "READY":
			return{"status":"READY"}
		elif message.startswith("ENROLL_OK:"):
			return{
				"status": "ENROLL_OK",
				"finger_id": int(message.split(":")[1])
			}
		elif message.startswith("ENROLL_FAIL:"):
			return{
				"status": "ENROLL_FAIL",
				"reason": message.split(":", 1)[1]
			}
		elif message in ("ENROLL_START", "PLACE_FINGER", "REMOVE_FINGER", "PLACE_AGAIN"):
			return{"status": message}
		return{
			"status":"UNKNOWN",
			"raw": message
		}
