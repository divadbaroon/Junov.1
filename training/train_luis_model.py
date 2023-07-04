import requests
import json
import os
import configuration.secrets.config as config

# Relativing relative paths to training data
utterance_file_path = os.path.join('luis_training_data/utterances.json')
pattern_file_path = os.path.join('luis_training_data/patterns.json')
entity_file_path = os.path.join('luis_training_data/entities.json')
intent_file_path = os.path.join('luis_training_data/intents.json')

class TrainLuisModel:
	"""
 	Creates and trains a fully functioning Azure LUIS model
	Training data is imported and used to train the LUIS models intent recognition.
	The model is mainly used for recognizing and responding to commands given by the user.
  	"""

	def __init__(self) -> None:
		"""Initializes the LUIS model"""
		# LUIS app information
		self.luis_app_id = config.retrieve_secret('NEW-LUIS-APP-ID')
		self.luis_key = config.retrieve_secret('LUIS-API')
		self.authoring_endpoint = 'https://westus.api.cognitive.microsoft.com/'
		self.app_version = '0.1'
		self.headers = {'Ocp-Apim-Subscription-Key': self.luis_key}
		self.params ={}
  
		# load in training data
		self._load_in_data()
  
	def train_luis_model(self) -> None:
		"""Creates and trains a LUIS model"""
  
		# load in the data
		self._load_in_data()

		# LUIS API only takes 100 utterances and patterns at a time
		self.utterance_data = self._split_data_into_chunks(self.utterance_data)
		self.pattern_data = self._split_data_into_chunks(self.pattern_data)
  
		# import the data into the LUIS model
		self._import_luis_data()
		# train the LUIS model
		#self._train_luis_model()
  
	def _load_in_data(self) -> None:
		"""Loads in the data to be imported into the LUIS model"""
  		# load in example utterances 
		with open(utterance_file_path) as f:
			self.utterance_data = json.load(f) 
		# load in example utterances 
		with open(pattern_file_path) as f:
			self.pattern_data = json.load(f) 
		# load in entities
		with open(entity_file_path) as f:
			self.entity_data = json.load(f) 
		# load in intents
		with open(intent_file_path) as f:
			self.intent_data = json.load(f) 
   
	def _split_data_into_chunks(self, data: list) -> list:
		"""Splits the utterance and pattern data into chunks of 100 utterances"""
		data_chunks = []
		
		# split the data into chunks of 100
		for i in range(0, len(data), 100):
				utterance_chunk = data[i:i + 100]
				data_chunks.append(utterance_chunk)
    
		return data_chunks
   
	def _import_luis_data(self) -> None:
		"""Creates the LUIS model and trains it"""
		# Make the REST call to import the LUIS model.
		self._import_luis_entities()
		self._import_luis_utterances()
		self._import_luis_patterns()

	def _import_luis_utterances(self) -> None:
		"""Imports the list of utterances into the LUIS model"""
		try:
      
			for chunk in range(len(self.utterance_data)):
				# Make the REST call to POST the list of example utterances.
				response = requests.post(f'{self.authoring_endpoint}luis/authoring/v3.0/apps/{self.luis_app_id}/versions/{self.app_version}/examples',
					headers=self.headers, params=self.params, data=json.dumps(self.utterance_data[chunk]))

			# Print the results on the console.
			print(response.json())
   
		except Exception as e:
			print(f'{e}')

	def _import_luis_patterns(self) -> None:
		"""Imports the list of patterns into the LUIS model"""
		try:
			for chunk in range(len(self.pattern_data)):
				# Make the REST call to POST the list of example utterances.
				response = requests.post(f'{self.authoring_endpoint}luis/authoring/v3.0/apps/{self.luis_app_id}/versions/{self.app_version}/patternrules',
					headers=self.headers, params=self.params, data=json.dumps(self.pattern_data[chunk]))

			# Print the results on the console.
			print(response.json())
   
		except Exception as e:
			print(f'{e}')

	def _import_luis_entities(self) -> None:
		"""Imports the list of entities into the LUIS model"""
		try:
			# Loop through the pattern.any entities
			for entity in self.entity_data:
				# Make the REST call to create each pattern.any entity.
				response = requests.post(
					f'{self.authoring_endpoint}luis/authoring/v3.0/apps/{self.luis_app_id}/versions/{self.app_version}/patternanyentities',
					headers=self.headers, params=self.params, json=entity)

				# Print the results on the console.
				print(f'Create pattern.any entity {entity["name"]}:')
				print(response.json())

		except Exception as e:
			print(f'{e}')
   
	def _import_luis_intents(self) -> None:
		"""Imports the list of intents into the LUIS model"""
		try:
			# Loop through each intent
			for intent in self.intent_data:
				# Make the REST call to create the intent
				response = requests.post(
					f'{self.authoring_endpoint}luis/authoring/v3.0/apps/{self.luis_app_id}/versions/{self.app_version}/intents',
					headers=self.headers, params=self.params, json=intent)
				
				# Print the results on the console.
				print(f'Created the intent: {intent["name"]}')
				print(response.json())

		except Exception as e:
			print(f'{e}')
   	
	def _train_luis_model(self) -> None:
		"""Begin a training session for the LUIS model"""
		# Make the REST call to initiate a training session.
		response = requests.post(f'{self.authoring_endpoint}luis/authoring/v3.0/apps/{self.luis_app_id}/versions/{self.app_version}/train',
			headers=self.headers, params=self.params, data=None)

		# Print the results on the console.
		print('Request training:')
		print(response.json())

		# Make the REST call to request the status of training.
		response = requests.get(f'{self.authoring_endpoint}luis/authoring/v3.0/apps/{self.luis_app_id}/versions/{self.app_version}/train',
			headers=self.headers, params=self.params, data=None)

		# Print the results on the console.
		print('Request training status:')
		print(response.json())


