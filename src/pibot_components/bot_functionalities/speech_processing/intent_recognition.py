import requests

class LuisIntentRecognition:
		"""
		luis_app_id (str): application id for Azure's LUIS service
		luis_key (str): subscription key for Azure's LUIS service
		"""

		def __init__(self, luis_app_id:str, luis_key:str):
			self.luis_app_id = luis_app_id
			self.luis_key = luis_key

		def get_user_intent(self, speech:str):
			"""
			Retrieves the similarity rankings between the user's speech and the trained LUIS model.
			:param speech: (str) speech input
			:return: (str) json file containing similarity rankings between the user's speech and the trained luis model
			"""

			if isinstance(speech, dict):
				speech = speech['translated_speech']

			endpoint_url = (f"https://westus.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/{self.luis_app_id}"
							f"/slots/production/predict?verbose=true&show-all-intents=true&log=true"
							f"&subscription-key={self.luis_key}"
							f"&query={speech}")

			response = requests.get(endpoint_url)
			# Check whether request was successful
			if response.status_code == 200:
				# Returned json file of the similarity rankings between the user's speech and the trained luis model
				intents_json = response.json()
			else:
				raise ValueError(f"The request sent to the LUIS model was unsuccessful. Error: {response.status_code}")

			return intents_json
