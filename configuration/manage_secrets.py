from .utils import AzureKeyVaultHandler, EnvironmentVariableHandler, LocalSecretHandler, DataHandler, AzureResourceManager
from .encryption import EncryptionHandler

class ConfigurationManager:
	"""
	used to manage and retrieve secrets from 'secret_config.yaml'
	"""
	def __init__(self):
		self.azure_key_vault = AzureKeyVaultHandler()
		self.environment_variables = EnvironmentVariableHandler()
		self.encryption_handler = EncryptionHandler()
		self.local_secrets = LocalSecretHandler(self.encryption_handler)
  
		self.data = DataHandler()._load_in_data()
		self.preferred_secret_storage = self.data['preferred_secret_storage']
		self.api_keys = self.data['api_keys']
  
	def initial_setup(self) -> None:
		"""
  		Peforms initial setup of the bot's secret values. This is performed after the necessary
		infrastrucutre has been created in Azure. The secrets values are initially stored in an Azure keyvault.
		and encrypted and stored locally for ease of use.
    	"""
		self.api_keys = AzureResourceManager()._retrieve_azure_secrets(self.api_keys)
		self.azure_key_vault._save_keyvault_secrets(self.api_keys)
		self.local_secrets._save_and_encrypt_local_secrets(self.api_keys)
  
	def retrieve_api_keys(self) -> dict:
		"""
  		used to retrieve the bot's secret values from Azure Key Vault, environment variables, or locally.
		secret values are stored in a hash map for ease of use
   		"""
		if self.preferred_secret_storage == 'azure':
			api_keys = self.azure_key_vault._get_keyvault_secrets(self.api_keys)
		elif self.preferred_secret_storage == 'environment':
			api_keys = self.environment_variables._get_environment_secrets(self.api_keys)
		elif self.preferred_secret_storage == 'local':
			api_keys = self.local_secrets._load_in_local_secrets()
		return api_keys 

	def retrieve_config_value(self, value) -> dict:
		"""
		used to retrieve the bot's configuration values from 'config.yaml'
		"""
		return self.data[value]

if __name__ == "__main__":
	ConfigurationManager().initial_setup()

