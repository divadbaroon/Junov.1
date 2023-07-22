import requests

class LuisIntentRecognition:
		"""
		A class that detects the user intent from the user's speech using the trained LUIS model.
		"""

		def __init__(self, api_keys: dict):
			self.api_keys = api_keys

		def get_user_intent(self, speech:str) -> dict:
			"""
			Retrieves the similarity rankings between the user's speech and the trained LUIS model.
			:param speech: (str) speech input
			:return: (dict) Dictionary containing similarity rankings between the user's speech and the trained luis model
			"""

			if isinstance(speech, dict):
				speech = speech['translated_speech']

			endpoint_url = (f"https://westus.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/{self.api_keys['LUIS-APPLICATION-ID']}"
							f"/slots/production/predict?verbose=true&show-all-intents=true&log=true"
							f"&subscription-key={self.api_keys['LUIS-API-KEY']}"
							f"&query={speech}")

			response = requests.get(endpoint_url)
			# Check whether request was successful
			if response.status_code == 200:
				# Returned json file of the similarity rankings between the user's speech and the trained luis model
				intents_data = response.json()
			else:
				raise ValueError(f"The request sent to the LUIS model was unsuccessful. Error: {response.status_code}")

			return intents_data
