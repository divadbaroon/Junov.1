from configuration.manage_secrets import DataHandler
from configuration.manage_secrets import AzureKeyVaultHandler
from configuration.manage_secrets import LocalSecretHandler
from configuration.manage_secrets import AzureResourceManager

class EncryptSecrets:
	
	def __init__(self):
		self.data = DataHandler()._load_in_data()
		self.preferred_secret_storage = self.data['preferred_secret_storage']
		self.api_keys = self.data['api_keys']
		self.api_keys = AzureResourceManager()._retrieve_azure_secrets(self.api_keys)
  
		self.azure_key_vault = AzureKeyVaultHandler()
		self.local_secrets = LocalSecretHandler()
  
	def _setup(self):
		self.azure_key_vault._save_keyvault_secrets(self.api_keys)
		self.local_secrets._save_and_encrypt_local_secrets(self.api_keys)
  
if __name__ == '__main__':
    EncryptSecrets()._setup()
