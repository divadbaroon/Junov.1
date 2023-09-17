import json
import os
import requests
import time
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations.authoring import ConversationAuthoringClient
from configuration.manage_secrets import ConfigurationManager

class TrainCLUModel:
	"""
 	Creates and trains a fully functioning Azure CLU model
	Training data is imported and used to train the CLU models intent recognition.
	The model is mainly used for recognizing and responding to commands given by the user.
  	"""

	def __init__(self, folder_name) -> None:
		"""Initializes the CLU model"""
  
		self.configuration_manager = ConfigurationManager()
		self.api_keys = self.configuration_manager.retrieve_api_keys()
		self.project_name  = self.api_keys['CLU-PROJECT-NAME']
		self.training_model_name = self.api_keys['CLU-TRAINING-MODEL-NAME']
		self.endpoint = self.api_keys['CLU-ENDPOINT']
		credential = AzureKeyCredential(self.api_keys['CLU-API-KEY'])
		self.client = ConversationAuthoringClient(self.endpoint, credential)
  
		self.data_handler = DataHandler()
		self.project_data = self.data_handler._prepare_training_data(folder_name)

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
			self._wait_for_operation_to_complete(operation_location, headers)
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
			self._wait_for_operation_to_complete(operation_location, headers)
		else:
			print(f"Deployment failed. Error: {response.json()}")
   
	def _wait_for_operation_to_complete(self, operation_location, headers):
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
   
class DataHandler:

	def _prepare_training_data(self, folder_name) -> dict:

		# Initialize assets
		assets = {
			"projectKind": "Conversation",
			"intents": [],
			"entities": [],
			"utterances": []
		}

		# Load in the training data
		# if project == 'assistant_training_data', load in the basic training data as well
		if folder_name == 'assistant_training_data':
			assets = self._load_in_project_data(folder_name, assets)
			assets = self._load_in_project_data('basic_training_data', assets)
		else:
			assets = self._load_in_project_data(folder_name, assets)

		return assets

	def _load_in_project_data(self, project, assets) -> dict:
		"""
		Loads in the project data from the project_header.json file
		"""
		# Walk through the directory tree
		for dirpath, dirnames, filenames in os.walk(f'training/{project}'):
			for filename in filenames:
				if filename.endswith('.json'):
					full_path = os.path.join(dirpath, filename)
					
					# Load the JSON data
					file_data = self._load_in_file(full_path)

					 # Merge the loaded data into assets based on the file type
					if filename == 'intents.json':
						assets["intents"].extend(file_data["intents"])
					elif filename == 'entities.json':
						assets["entities"].extend(file_data)  
					elif filename == 'utterances.json':
						assets["utterances"].extend(file_data)
		return assets

	def _load_in_file(self, file_path) -> dict:
		with open(file_path, 'r') as f:
			return json.load(f)

if __name__ == "__main__":
	
	folder_name = input("Enter the name of the folder used for training (i.e 'assistant_training_data', 'basic_training_data'): ")
	
	new_model = TrainCLUModel(folder_name)
	new_model.import_project_data()
	new_model.train_conversation_model()
	new_model.deploy_conversation_model()
