import json
import os
import requests
import time

from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations.authoring import ConversationAuthoringClient

from configuration.manage_secrets import ConfigurationManager

# Relativing relative paths to training data
project_header_path = os.path.join('training/assistant_training_data/project_header.json')
utterance_file_path = os.path.join('training/assistant_training_data/utterances.json')
patterns_file_path = os.path.join('training/assistant_training_data/patterns.json')
entity_file_path = os.path.join('training/assistant_training_data/entities.json')
intent_file_path = os.path.join('training/assistant_training_data/intents.json')

class TrainLuisModel:
	"""
 	Creates and trains a fully functioning Azure LUIS model
	Training data is imported and used to train the LUIS models intent recognition.
	The model is mainly used for recognizing and responding to commands given by the user.
  	"""

	def __init__(self) -> None:
		"""Initializes the LUIS model"""
  
		self.configuration_manager = ConfigurationManager()
		self.api_keys = self.configuration_manager.retrieve_api_keys()
		print(self.api_keys)
		self.endpoint = self.api_keys['CLU-ENDPOINT']
		credential = AzureKeyCredential(self.api_keys['CLU-API-KEY'])
		self.client = ConversationAuthoringClient(self.endpoint, credential)

		self.project_name  = self.api_keys['CLU-PROJECT-NAME']
		self.project_data = self._load_in_project_data()
  
		self.training_model_name = self.api_keys['CLU-TRAINING-MODEL-NAME']
  
	def import_project_data(self) -> None:
		"""
		Creates a new CLU project and imports the training data located within 
  		the /training sub-directory into it
		"""
		poller = self.client.begin_import_project(
				project_name=self.project_name,
				project={
					"assets": self.project_data,
					"stringIndexType": "Utf16CodeUnit",
					"metadata": {
						"projectKind": "Conversation",
						"settings": {"confidenceThreshold": 0.7},
						"projectName": self.project_name,
						"multilingual": True,
						"description": "Trying out CLU",
						"language": "en-us",
					},
					"projectFileVersion": "2022-05-01",
				},
		)
		print(f"\nImporting training data to project: {self.project_name}")
		print(f'\n{poller.result()}')

	def train_conversation_model(self):
		"""
		Begins a training session for the newly created CLU model
		"""	

		url = f"{self.endpoint}/language/authoring/analyze-conversations/projects/{self.project_name}/:train?api-version=2022-10-01-preview"

		headers = {
			"Ocp-Apim-Subscription-Key": self.api_keys['CLU-API-KEY'],
			"Content-Type": "application/json"
		}

		body = {
			"modelLabel": self.training_model_name,
			"trainingMode": "standard",
			"evaluationOptions": {
				"kind": "percentage",
				"testingSplitPercentage": 20,
				"trainingSplitPercentage": 80
			}
		}

		print(f"\nBeginning a training session for the project: {self.project_name}")
		response = requests.post(url, headers=headers, json=body)

		if response.status_code == 202:
			operation_location = response.headers["operation-location"]
			print(f"\nTraining started. Poll the operation location to get status: {operation_location}")
			self.wait_for_operation_to_complete(operation_location, headers)
		else:
			print(f"Training failed. Error: {response.json()}")
   
	def deploy_conversation_model(self):
		"""
		Deploys the newly created CLU model
		"""    

		url = f"{self.endpoint}/language/authoring/analyze-conversations/projects/{self.project_name}/deployments/{self.training_model_name}?api-version=2023-04-01"

		headers = {
			"Ocp-Apim-Subscription-Key": self.api_keys['CLU-API-KEY'],
			"Content-Type": "application/json"
		}

		body = {
			"trainedModelLabel": self.training_model_name
		}

		print(f"\nDeploying the model: {self.training_model_name}")
		response = requests.put(url, headers=headers, json=body)  

		if response.status_code == 202:
			operation_location = response.headers["operation-location"]
			print(f"\nDeployment started. Poll the operation location to get status: {operation_location}")
			self.wait_for_operation_to_complete(operation_location, headers)
		else:
			print(f"Deployment failed. Error: {response.json()}")

  
	def _load_in_project_data(self) -> dict:
		# Load in project_header information
		with open(project_header_path) as f:
			project_header = json.load(f) 

		# Load in example utterances 
		with open(utterance_file_path) as f:
			utterance_data = json.load(f) 
	
		# Load in example patterns
		with open(patterns_file_path) as f:
			pattern_data = json.load(f)

		# Load in entities
		with open(entity_file_path) as f:
			entity_data = json.load(f) 

		# Load in intents
		with open(intent_file_path) as f:
			intent_data = json.load(f) 

		# Initialize an empty 'assets' dictionary within project_data
		project_data = {}

		# Update 'assets' with the various types of data
		project_data["projectKind"] = "Conversation"
		project_data["intents"] = intent_data["intents"]  # Assuming intent_data is a dictionary containing an 'intents' key
		project_data["entities"] = entity_data
		project_data["utterances"] = utterance_data + pattern_data

		# Save the project data to a file
		return project_data
   
	def wait_for_operation_to_complete(self, operation_location, headers):
		while True:
			time.sleep(5)  # Wait for 5 seconds before checking the status again
			response = requests.get(operation_location, headers=headers)
			status = response.json().get("status")
			if status == "succeeded":
				print("Operation completed successfully.")
				break
			elif status == "failed":
				print("Operation failed.")
				break
   
if __name__ == "__main__":
	"""
	Runs the training session
	"""
	print("\nImporting training data from the /training sub-directory into a new CLU project for training and deployment.")
	print("Please note: The entire process may take up to 5 minutes to complete.")

 
	test = TrainLuisModel()
	test.import_project_data()
	test.train_conversation_model()
	test.deploy_conversation_model()


  
	