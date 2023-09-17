from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class KeyVaultManager:
	"""
	used to manage and retrieve secrets from Azure Key Vault
	"""
	
	def __init__(self):
		vault_url = f"https://Juno-vault.vault.azure.net/"
		credential = DefaultAzureCredential()
		self.client = SecretClient(vault_url=vault_url, credential=credential)
		
	def retrieve_secret(self, secret_name:str) -> str:
		"""
		retrieve secret from Azure Key vault
		"""
		secret = self.client.get_secret(secret_name)
		return secret.value

	def create_secret(self, secret_name:str, value: str) -> None:
		"""
		create new secret in Azure Key vault with an associated value
		"""
		self.client.set_secret(secret_name, value)