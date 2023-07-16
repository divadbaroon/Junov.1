import yaml
import os
import configuration.secrets.config as config

# Construct the path to the 'secret_config.yaml'
current_directory = os.path.dirname(os.path.abspath(__file__))
secret_config_path = os.path.join(current_directory, 'secret_config.yaml')

class ConfigurationManager:
	"""
	Configures and saves necessary properties to secret_config.yaml
	"""
	def __init__(self):
		self.data = self.load_in_data()
		self.preferred_secret_storage = self.data['preferred_secret_storage']
		self.api_key = self.data['api_keys']

	def load_in_data(self):
		"""Load in data from 'secret_config.yaml'"""
		try:
			with open(secret_config_path, "r") as f:
				return yaml.safe_load(f)
		except FileNotFoundError:
			print('The file "secret_config.yaml" is missing.\nMake sure all files are located within the same folder.')
	
	def load_api_keys(self) -> dict:
		"""Retrieving the bot's secret values from Azure Key Vault.
			Secret values are stored in a hash map for ease of use"""
		if self.preferred_secret_storage == 'azure':
			api_keys = self._get_keyvault_secrets()
		elif self.preferred_secret_storage == 'environment':
			api_keys = self._get_local_secrets()
		return api_keys 
		 
	def _get_keyvault_secrets(self) -> dict:
		"""
		Load secrets from Azure keyvault
		"""
		api_keys= {}
		for name in self._secret_names():
			self.api_key[name] = config.retrieve_secret(name)
		return api_keys

	def _get_local_secrets(self) -> dict:
		"""
		Load secrets from environment variables
		"""
		api_keys= {}
		for name in self._secret_names():
			self.api_key[name] = os.getenv(name)
		return api_keys

	def _secret_names(self) -> list:
		"""Retrieve the names of the keys in the api_keys dictionary"""
		return list(self.api_key.keys())

