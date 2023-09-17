from cryptography.fernet import Fernet
import yaml

encryption_key_path = 'configuration/secrets/key.key'
  
class EncryptionHandler:
  
	def _save_key(self):
		# Save the key
		key = Fernet.generate_key()
		with open(encryption_key_path, "wb") as key_file:
			key_file.write(key)
   
		return key
   
	def _retrieve_key(self):
		# load the previously generated key
		with open(encryption_key_path, "rb") as key_file:
			key = key_file.read()
		return key
	
	def save_and_encrypt_local_secrets(self, api_keys):
	 
		encrypted_local_data_path = 'configuration/secrets/encrypted_secret_data.yaml'
  
		key = self._save_key()
		cipher_suite = Fernet(key)
  
		encrypted_api_keys = self._encrypt_api_keys(api_keys, cipher_suite)
	 
		with open(encrypted_local_data_path, 'w') as f:
			yaml.dump({'Encrypted API Keys': encrypted_api_keys}, f)
   
		print('Local secrets have been encrypted and saved to: "configuration/secrets/encrypted_local_data.yaml"')
		print('It is highly recommended that your remove api keys from the file: "configuration/secrets/local_data.yaml"')
   	
	def load_in_encrypted_secrets(self) -> dict:
	 
		encrypted_local_data_path = 'configuration/secrets/encrypted_secret_data.yaml'
  
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
		decrypted_api_keys = {}
		for key, value in encrypted_api_keys.items():
			if value is not None:
				decrypted_api_keys[key] = cipher_suite.decrypt(value.encode()).decode()
			else:
				decrypted_api_keys[key] = None
		return decrypted_api_keys

  

