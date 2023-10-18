from .utils.secret_retrieval_handler import SecretRetrieval
from .utils.encryption_handler import EncryptionHandler
from .utils.key_vault_handler import KeyVaultManager

class ConfigurationManager:
	"""
	used to manage and retrieve secrets from 'secret_config.yaml'
	"""
	def __init__(self):
		self.encryption_handler = EncryptionHandler()
		self.secret_manager = SecretRetrieval(self.encryption_handler)
  
		self.data = self.secret_manager._load_in_data()
		self.key_vault = KeyVaultManager(self.retrieve_config_value('KEYVAULT_NAME'))
		self.preferred_secret_storage = self.data['preferred_secret_storage']
		self.api_keys = self.data['api_keys']
  
	def initial_setup(self) -> None:
		"""
  		Peforms initial setup of the bot's secret values. This is performed after the necessary
		infrastrucutre has been created in Azure. The secrets values are initially stored in an Azure keyvault.
		and encrypted and stored locally for ease of use.
    	"""
		self.api_keys = self.secret_manager._get_azure_secrets(self.api_keys, self.key_vault)
		self.secret_manager._get_keyvault_secrets(self.api_keys, self.key_vault)
		self.secret_manager._save_and_encrypt_local_secrets(self.api_keys)
  
	def retrieve_api_keys(self) -> dict:
		"""
  		used to retrieve the bot's secret values from Azure Key Vault, environment variables, or locally.
		secret values are stored in a hash map for ease of use
   		"""
		if self.preferred_secret_storage == 'azure':
			api_keys = self.secret_manager._get_keyvault_secrets(self.api_keys, self.key_vault_name)
		elif self.preferred_secret_storage == 'environment':
			api_keys = self.secret_manager._get_environment_secrets(self.api_keys)
		elif self.preferred_secret_storage == 'local':
			api_keys = self.secret_manager._load_in_local_secrets()
		return api_keys 

	def retrieve_config_value(self, value) -> dict:
		"""
		used to retrieve the bot's configuration values from 'config.yaml'
		"""
		return self.data[value]

if __name__ == "__main__":
	ConfigurationManager().initial_setup()

