"""
Note:
In order to be authenitcated you must be signed into your Azure account.
To sign in, run the command: 'az login' into your terminal

The following secrets need to be stored in your Azure Key Vault for the bot to function properly:
- Azure Speech Service API key 
- Azure LUIS API key
- Azure LUIS APP ID
- OpenAI API key 
- OpenWeatherMap API key
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
