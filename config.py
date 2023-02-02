from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
		
def retrieve_secret(secret_name:str) -> str:
	"""
	Retrieve secret from Azure Key vault
	:param query: (str) name of secret
	:return: (str) secret value
	"""
	key_vault = "https://pikeys.vault.azure.net/"
	credential = DefaultAzureCredential()
	client = SecretClient(vault_url=key_vault, credential=credential)
	secret = client.get_secret(secret_name)
	return secret.value