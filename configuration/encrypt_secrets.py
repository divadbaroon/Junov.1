from configuration.manage_secrets import DataHandler
from configuration.manage_secrets import AzureKeyVaultHandler
from configuration.manage_secrets import LocalSecretHandler
from configuration.manage_secrets import AzureResourceManager
from cryptography.fernet import Fernet
import yaml
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_directory, 'secrets', 'key.key')

class EncryptSecrets:
	
	def __init__(self):
		self.data = DataHandler()._load_in_data()
		self.preferred_secret_storage = self.data['preferred_secret_storage']
		self.api_keys = self.data['api_keys']
		self.api_keys = AzureResourceManager()._retrieve_azure_secrets(self.api_keys)
  
		self.azure_key_vault = AzureKeyVaultHandler()
		self.encryption_handler = EncryptionHandler()
		self.local_secrets = LocalSecretHandler(self.encryption_handler)
  
	def _setup(self):
		self.azure_key_vault._save_keyvault_secrets(self.api_keys)
		self.local_secrets._save_and_encrypt_local_secrets(self.api_keys)
  
class EncryptionHandler:
  
	def _save_key(self):
		# Save the key
		key = Fernet.generate_key()
		with open(key_path, "wb") as key_file:
			key_file.write(key)
   
		return key
   
	def _retrieve_key(self):
		# load the previously generated key
		with open(key_path, "rb") as key_file:
			key = key_file.read()
		return key
	
	def save_and_encrypt_local_secrets(self, api_keys):
	 
		encrypted_local_data_path = 'configuration/secrets/encrypted_local_data.yaml'
  
		key = self._save_key()
		cipher_suite = Fernet(key)
  
		encrypted_api_keys = self._encrypt_api_keys(api_keys, cipher_suite)
	 
		with open(encrypted_local_data_path, 'w') as f:
			yaml.dump({'Encrypted API Keys': encrypted_api_keys}, f)
   
		print('Local secrets have been encrypted and saved to: "configuration/secrets/encrypted_local_data.yaml"')
		print('It is highly recommended that your remove api keys from the file: "configuration/secrets/local_data.yaml"')
   	
	def load_in_encrypted_secrets(self) -> dict:
	 
		encrypted_local_data_path = 'configuration/secrets/encrypted_local_data.yaml'
  
		key = self._retrieve_key()
		cipher_suite = Fernet(key)
  
		with open(encrypted_local_data_path, 'r') as f:
			encrypted_api_keys = yaml.safe_load(f)
   
		return self._decrypt_api_keys(encrypted_api_keys['Encrypted API Keys'], cipher_suite )

	def _encrypt_api_keys(self, api_keys, cipher_suite):
		"""
		encrypts api keys
		"""
		encrypted_api_keys = {key: cipher_suite.encrypt(value.encode()).decode() if value is not None else None for key, value in api_keys.items()}
		return encrypted_api_keys

	def _decrypt_api_keys(self, encrypted_api_keys, cipher_suite):
		"""
		encrypts api keys
		"""
		decrypted_api_keys = {key: cipher_suite.decrypt(value.encode()).decode() for key, value in encrypted_api_keys.items()}
		return decrypted_api_keys
  
if __name__ == '__main__':
    EncryptSecrets()._setup()
