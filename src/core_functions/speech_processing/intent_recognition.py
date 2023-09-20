from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

class CLUIntentRecognition:
		"""
		A class that detects the user intent from the user's speech using the trained CLU model.
		"""

		def __init__(self, api_keys: dict, profile_settings:object, voice_settings:object):	
			# Load in secrets needed to use the CLU model
			self._load_in_secrets(api_keys)	 
			# Initialize CLU client
			self.client = ConversationAnalysisClient(self.clu_endpoint, self.clu_key)
			# load in profile and voice settings
			self.profile_settings = profile_settings
			self.voice_settings = voice_settings

		def get_user_intent(self, speech:str) -> dict:
			"""
			Retrieves the similarity rankings between the user's speech and the trained CLU model.
			:param speech: (str) speech input
			:return: (dict) Dictionary containing similarity rankings between the user's speech and the trained CLU model
			"""

			# Create job to send to CLU model
			job = {
					"kind": "Conversation",
					"analysisInput": {
						"conversationItem": {
							"participantId": "1",
							"id": "1",
							"modality": "text",
							"language": self._get_current_language(),
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

			# Similarity rankings between the user's speech and the trained CLU model
			return self.client.analyze_conversation(task=job)

		def _load_in_secrets(self, api_keys:dict) -> None:
			"""
			Initializes secrets needed to use the CLU model.
			"""
			self.api_keys = api_keys
			self.clu_endpoint = self.api_keys['CLU-ENDPOINT']
			self.clu_key = AzureKeyCredential(self.api_keys['CLU-API-KEY'])
			self.clu_project_name = self.api_keys['CLU-PROJECT-NAME']
			self.clu_deployment_name = self.api_keys['CLU-TRAINING-MODEL-NAME']
   
		def _get_current_language(self) -> str:
			"""
			Retrieves the current language being used by the bot.
			"""
			language  = self.profile_settings.retrieve_property('current_language')
			return self.voice_settings.retrieve_language_code(language)


