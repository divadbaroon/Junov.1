import yaml
import os
import configuration.secrets.config as config

# Construct the path to the 'secret_config.yaml'
current_directory = os.path.dirname(os.path.abspath(__file__))
secret_config_path = os.path.join(current_directory, 'secret_config.yaml')

class ConfigureSecrets():
   """Configures and saves necessary api keys"""
   
   def __init__(self):
      self.data = self.load_in_data()
      self.preferred_secret_storage = self.data['preferred_secret_storage']
      
   def load_in_data(self):
      """Load in data from 'secret_config.yaml'"""
      try:
         with open(secret_config_path, "r") as f:
               return yaml.safe_load(f)
      except FileNotFoundError:
         print('The file "secret_config.yaml" is missing.\nMake sure all files are located within the same folder.')
     
   def load_apia_keys(self) -> dict:
      """Retrieving the bot's secret values from Azure Key Vault
         storing the bot's secret values in a hash map for ease of use"""
      if self.preferred_secret_storage == 'azure':
         api_keys = self._keyvault_secrets()
      elif self.preferred_secret_storage == 'environment':
         api_keys = self._get_local_variables()
      return api_keys  
         
   def _keyvault_secrets(self) -> dict:
      """
      Load secrets from Azure keyvault
      """
      api_keys= {}
      api_keys['region'] = 'eastus'
      api_keys['cognitive_services_api'] = config.retrieve_secret('Cognitive-Services-API')
      api_keys['luis_app_id'] = config.retrieve_secret('LUIS-App-ID')
      api_keys['luis_key'] = config.retrieve_secret('LUIS-API')
      api_keys['openai_key'] = config.retrieve_secret('OpenAI-API')
      api_keys['weather_key'] = config.retrieve_secret('Weather-API')
      api_keys['translator_key'] = config.retrieve_secret('Translator-API')
      api_keys['elevenlabs_api_key'] = config.retrieve_secret('Elevenlabs-API-Key')
      api_keys['news_key'] = config.retrieve_secret('News-Key')
      api_keys['spotify_client_id'] = config.retrieve_secret('Spotify-clientID')
      api_keys['spotify_client_secret'] = config.retrieve_secret('Spotify-clientsecret')
      return api_keys

   def _get_local_variables(self) -> dict:
      """
      Load secrets from environment variables
      """
      api_keys= {}
      api_keys['region'] = 'eastus'
      api_keys['cognitive_services_api'] = os.getenv('Cognitive-Services-API')
      api_keys['luis_app_id'] = os.getenv('LUIS-App-ID')
      api_keys['luis_key'] = os.getenv('LUIS-API')
      api_keys['openai_key'] = os.getenv('OpenAI-API')
      api_keys['weather_key'] = os.getenv('Weather-API')
      api_keys['translator_key'] = os.getenv('Translator-API')
      api_keys['elevenlabs_api_key'] = os.getenv('Elevenlabs-API-Key')
      api_keys['spotify_client_id'] = config.retrieve_secret('Spotify-clientID')
      api_keys['spotify_client_secret'] = config.retrieve_secret('Spotify-clientsecret')
      return api_keys
