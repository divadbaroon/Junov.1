import yaml
import os
from configuration.secrets.config import KeyVaultManager

# path to 'secret_config.yaml'
current_directory = os.path.dirname(os.path.abspath(__file__))
secret_config_path = os.path.join(current_directory, 'secrets', 'secret_config.yaml')

class ConfigurationManager:
	"""
	used to manage and retrieve secrets from 'secret_config.yaml'
	"""
	def __init__(self):
		self.key_vault = KeyVaultManager()
		self.data = self._load_in_data()
		self.preferred_secret_storage = self.data['preferred_secret_storage']
		self.api_keys = self.data['api_keys']
  
	def retrieve_api_keys(self) -> dict:
		"""
  		used to retrieve the bot's secret values from Azure Key Vault or environment variables
		secret values are stored in a hash map for ease of use
   		"""
		if self.preferred_secret_storage == 'azure':
			api_keys = self._get_keyvault_secrets()
		elif self.preferred_secret_storage == 'environment':
			api_keys = self._get_local_secrets()
   
		api_keys['region'] = 'eastus'
		return api_keys 

	def _load_in_data(self):
		"""
  		load in data from 'secret_config.yaml'
    	"""
		try:
			with open(secret_config_path, "r") as f:
				return yaml.safe_load(f)
		except FileNotFoundError:
			print('The file: "secret_config.yaml" was not found. Ensure the file is located within the "configuration/secrets" directory')
		 
	def _get_keyvault_secrets(self) -> dict:
		"""
		Retrieve secrets from Azure keyvault
		"""
		for secret in self.api_keys.keys():
			if self.api_keys[secret] is not None:
				self.key_vault.create_secret(secret, self.api_keys[secret])
			try:
				self.api_keys[secret] = self.key_vault.retrieve_secret(secret)
			except:
				self.api_keys[secret] = None
		return self.api_keys

	def _get_local_secrets(self) -> dict:
		"""
		Retrieve secrets from environment variables
		"""
		for secret in self.api_keys.keys():
			if self.api_keys[secret] is not None:
				os.environ[secret] = self.api_keys[secret]
			try:
				self.api_keys[secret] = os.getenv(secret)
			except:
				self.api_keys[secret] = None
		return self.api_keys
