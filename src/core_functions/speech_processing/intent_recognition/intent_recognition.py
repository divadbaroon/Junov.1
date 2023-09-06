from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

class LuisIntentRecognition:
		"""
		A class that detects the user intent from the user's speech using the trained LUIS model.
		"""

		def __init__(self, api_keys: dict):	
			self.api_keys = api_keys
			self.clu_endpoint = self.api_keys['CLU-ENDPOINT']
			self.clu_key = AzureKeyCredential(self.api_keys['CLU-API-KEY'])
			self.clu_project_name = self.api_keys['CLU-PROJECT-NAME']
			self.clu_deployment_name = self.api_keys['CLU-TRAINING-MODEL-NAME']   
			self.client = ConversationAnalysisClient(self.clu_endpoint, self.clu_key)

		def get_user_intent(self, speech:str) -> dict:
			"""
			Retrieves the similarity rankings between the user's speech and the trained LUIS model.
			:param speech: (str) speech input
			:return: (dict) Dictionary containing similarity rankings between the user's speech and the trained luis model
			"""
			
			if isinstance(speech, dict):
				speech = speech['translated_speech']
    
			query = speech

			result = self.client.analyze_conversation(
				task={
					"kind": "Conversation",
					"analysisInput": {
						"conversationItem": {
							"participantId": "1",
							"id": "1",
							"modality": "text",
							"language": "en",
							"text": query
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
		
			return result


