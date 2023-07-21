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
		self.api_keys = self.data['api_keys']

	def load_in_data(self):
		"""
  		Load in data from 'secret_config.yaml
    		'"""
		try:
			with open(secret_config_path, "r") as f:
				return yaml.safe_load(f)
		except FileNotFoundError:
			print('The file "secret_config.yaml" is missing.\nMake sure all files are located within the same folder.')
	
	def load_api_keys(self) -> dict:
		"""
  		Retrieving the bot's secret values from Azure Key Vault.
		Secret values are stored in a dictionary for ease of use
   		"""
		if self.preferred_secret_storage == 'azure':
			api_keys = self._get_keyvault_secrets()
		elif self.preferred_secret_storage == 'environment':
			api_keys = self._get_local_secrets()
   
		api_keys['region'] = 'eastus'
		return api_keys 
		 
	def _get_keyvault_secrets(self) -> dict:
		"""
		Load secrets from Azure keyvault
		"""
		for secret in self.api_keys.keys():
			try:
				self.api_keys[secret] = config.retrieve_secret(secret)
			except:
				self.api_keys[secret] = None
		return self.api_keys

	def _get_local_secrets(self) -> dict:
		"""
		Load secrets from environment variables
		"""
		for secret in self.api_keys.keys():
			try:
				self.api_keys[secret] = os.getenv(secret)
			except:
				self.api_keys[secret] = None
		return self.api_keys
