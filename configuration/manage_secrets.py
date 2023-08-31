import yaml
import os
from cryptography.fernet import Fernet
from configuration.secrets.config import KeyVaultManager

# path to 'secret_config.yaml'
current_directory = os.path.dirname(os.path.abspath(__file__))
secret_config_path = os.path.join(current_directory, 'secrets', 'secret_config.yaml')
key_path = os.path.join(current_directory, 'secrets', 'key.key')

class DataHandler:
		
	def _load_in_data(self):
		"""
  		load in data from 'secret_config.yaml'
		"""
		try:
			with open(secret_config_path, "r") as f:
				return yaml.safe_load(f)
		except FileNotFoundError:
			print('The file: "secret_config.yaml" was not found. Ensure the file is located within the "configuration/secrets" directory')
   
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
	
class AzureKeyVaultHandler:
	
	def __init__(self):
		self.key_vault = KeyVaultManager()
  
	def _save_keyvault_secrets(self, api_keys):
		for secret in api_keys.keys():
			if api_keys[secret] is not None:
				self.key_vault.create_secret(secret, api_keys[secret])

	def _get_keyvault_secrets(self, api_keys) -> dict:
		"""
		Retrieve secrets from Azure keyvault
		"""
		for secret in api_keys.keys():
			if api_keys[secret] is not None:					
				self.key_vault.create_secret(secret, api_keys[secret])
			try:
				api_keys[secret] = self.key_vault.retrieve_secret(secret)
			except:
				api_keys[secret] = None
		return api_keys

class EnvironmentVariableHandler:

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

class LocalSecretHandler:
	
	def __init__(self):
		self.encryption_handler = EncryptionHandler()
	
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

class AzureResourceManager:
	
	def __init__(self):
		self.key_vault = KeyVaultManager()
  
	def _retrieve_azure_secrets(self, api_keys):
		api_keys['COGNITIVE-SERVICES-API-KEY'] = self.key_vault.retrieve_secret('COGNITIVE-SERVICES-API-KEY')
		api_keys['TRANSLATOR-API-KEY'] = self.key_vault.retrieve_secret('TRANSLATOR-API-KEY')
		return api_keys

class ConfigurationManager:
	"""
	used to manage and retrieve secrets from 'secret_config.yaml'
	"""
	def __init__(self):
		self.azure_key_vault = AzureKeyVaultHandler()
		self.environment_variables = EnvironmentVariableHandler()
		self.local_secrets = LocalSecretHandler()
  
		self.data = DataHandler()._load_in_data()
		self.preferred_secret_storage = self.data['preferred_secret_storage']
		self.api_keys = self.data['api_keys']
  
	def retrieve_api_keys(self) -> dict:
		"""
  		used to retrieve the bot's secret values from Azure Key Vault or environment variables
		secret values are stored in a hash map for ease of use
   		"""
		if self.preferred_secret_storage == 'azure':
			api_keys = self.azure_key_vault._get_keyvault_secrets(self.api_keys)
		elif self.preferred_secret_storage == 'environment':
			api_keys = self.environment_variables._get_environment_secrets(self.api_keys)
		elif self.preferred_secret_storage == 'local':
			api_keys = self.local_secrets._load_in_local_secrets()
		return api_keys 
