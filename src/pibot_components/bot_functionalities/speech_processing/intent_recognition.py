from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
import requests

class LuisIntentRecognition:
		"""
		luis_app_id (str): application id for Azure's LUIS service
		luis_key (str): subscription key for Azure's LUIS service
		"""

		def __init__(self):
			self.luis_app_id = '0e62c7fd-5ec9-4a85-b517-b04ec9746a2f'
			self.luis_key = 'c9d134fdbc2b414b903665c6111ee5f5'

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

class CLUIntentRecognition:
	"""
	A class that retrieves the similarity rankings between the user's speech and the trained CLU model
	as a json file.
	
	Attributes:
	region (str): region used for Azure resources
	clu_endpoint (str): endpoint for Azure's CLU service
	clu_project_name (str): project name for Azure's CLU service
	clu_deployment_name (str): sdeployment name for Azure's CLU service
	clu_key (str): subscription key for Azure's CLU service
	"""
  
	def __init__(self, clu_endpoint:str, clu_project_name:str, clu_deployment_name:str, clu_key:str):
		self.clu_endpoint = clu_endpoint
		self.clu_project_name = clu_project_name
		self.clu_deployment_name = clu_deployment_name
		self.clu_key = clu_key

	def get_user_intent(self, speech:str):
		"""
		Retrieves the similarity rankings between the user's speech and the trained CLU model.
		:param speech: (str) speech input
		:return: (str) json file containing similarity rankings between the user's speech and the trained CLU model
		"""

		client = ConversationAnalysisClient(self.clu_endpoint, AzureKeyCredential(self.clu_key))

		result = client.analyze_conversation(
			task={
				"kind": "Conversation",
				"analysisInput": {
					"conversationItem": {
					"participantId": "1",
					"id": "1",
					"modality": "text",
					"language": "en",
					"text": speech
					},
				"isLoggingEnabled": False
					},
					"parameters": {
						"projectName": self.clu_project_name,
						"deploymentName": self.clu_deployment_name,
						"verbose": True
					}
				}
			)
		intents_json = result
		return intents_json["result"]