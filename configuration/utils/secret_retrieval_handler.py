import os
import yaml

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
secret_config_path = os.path.join(parent_directory, 'config.yaml')

class SecretRetrieval:
	"""
	Class used to retrieve secrets from various sources
	"""
	
	def __init__(self, encryption_handler:object):
		self.encryption_handler = encryption_handler
		self.data = self._load_in_data()

	def _get_keyvault_secrets(self, api_keys, key_vault:object) -> dict:
		"""
		Retrieve secrets from Azure keyvault
		"""
		for secret in api_keys.keys():
			if api_keys[secret] is not None:					
				key_vault.create_secret(secret, api_keys[secret])
			try:
				api_keys[secret] = key_vault.retrieve_secret(secret)
			except:
				api_keys[secret] = None
		return api_keys

	def _get_environment_secrets(self, api_keys) -> dict:
		"""
		Retrieve secrets from environment variables
		"""
		for secret in api_keys.keys():
			if api_keys[secret] is not None:
				os.environ[secret] = api_keys[secret]
			try:
				api_keys[secret] = os.getenv(secret)
			except:
				api_keys[secret] = None
		return api_keys

	def _get_azure_secrets(self, api_keys, key_vault:object) -> dict:
		"""
		Retrieve secrets from infra that was created in Azure
		"""
		api_keys['COGNITIVE-SERVICES-API-KEY'] = key_vault.retrieve_secret('COGNITIVE-SERVICES-API-KEY')
		api_keys['TRANSLATOR-API-KEY'] = key_vault.retrieve_secret('TRANSLATOR-API-KEY')
		api_keys['CLU-API-KEY'] = key_vault.retrieve_secret('CLU-API-KEY')
		api_keys['CLU-ENDPOINT'] = key_vault.retrieve_secret('CLU-ENDPOINT')
		api_keys['CLU-PROJECT-NAME'] = self.data['CLU_PROJECT_NAME']
		api_keys['CLU-TRAINING-MODEL-NAME'] = self.data['CLU_TRAINING_MODEL_NAME']
		api_keys['CLU-DEPLOYMENT-NAME'] = self.data['CLU_DEPLOYMENT_NAME']
		api_keys['REGION'] = self.data['REGION']
		return api_keys

	def _save_and_encrypt_local_secrets(self, api_keys):
		"""
		encrypts and saves secrets to local file
		"""
		self.encryption_handler.save_and_encrypt_local_secrets(api_keys)
  
	def _load_in_local_secrets(self) -> dict:
		"""
		loads in encrypted secrets from local file
		"""
		return self.encryption_handler.load_in_encrypted_secrets()

	def _load_in_data(self):
		"""
  		load in data from 'config.yaml'
		"""
		try:
			with open(secret_config_path, "r") as f:
				return yaml.safe_load(f)
		except FileNotFoundError:
			print('The file: "config.yaml" was not found. Ensure the file is located within the "configuration/secrets" directory')
