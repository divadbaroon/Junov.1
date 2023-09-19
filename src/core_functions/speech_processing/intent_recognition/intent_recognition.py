from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

class LuisIntentRecognition:
		"""
		A class that detects the user intent from the user's speech using the trained LUIS model.
		"""

		def __init__(self, api_keys: dict, profile_settings:object, voice_settings:object):	
			self.api_keys = api_keys
			self.clu_endpoint = self.api_keys['CLU-ENDPOINT']
			self.clu_key = AzureKeyCredential(self.api_keys['CLU-API-KEY'])
			self.clu_project_name = self.api_keys['CLU-PROJECT-NAME']
			self.clu_deployment_name = self.api_keys['CLU-TRAINING-MODEL-NAME']   
			self.client = ConversationAnalysisClient(self.clu_endpoint, self.clu_key)
			self.profile_settings = profile_settings
			self.voice_settings = voice_settings

		def get_user_intent(self, speech:str) -> dict:
			"""
			Retrieves the similarity rankings between the user's speech and the trained LUIS model.
			:param speech: (str) speech input
			:return: (dict) Dictionary containing similarity rankings between the user's speech and the trained luis model
			"""
			
			language  = self.profile_settings.retrieve_property('language')
			language_code = self.voice_settings.retrieve_language_code(language)
    
			query = speech

			result = self.client.analyze_conversation(
				task={
					"kind": "Conversation",
					"analysisInput": {
						"conversationItem": {
							"participantId": "1",
							"id": "1",
							"modality": "text",
							"language": language_code,
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


