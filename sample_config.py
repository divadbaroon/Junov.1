"""
Note:
In order to be authenitcated you must be signed into your Azure account.
To login type: az login
"""

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
		
def retrieve_secret(secret_name:str) -> str:
	"""
	Retrieve secret from Azure Key vault
	:param query: (str) name of secret
	:return: (str) secret value
	"""
	vault_name = 'your key vault name'
	key_vault = f"https://{vault_name}.vault.azure.net/"
	credential = DefaultAzureCredential()
	client = SecretClient(vault_url=key_vault, credential=credential)
	secret = client.get_secret(secret_name)
	return secret.value
