import configuration.secrets.config as config

def load_api_keys() -> dict:
    """Retrieving the bot's secret values from Azure Key Vault
       storing the bot's secret values in a hash map for ease of use"""
    api_keys= {}
    api_keys['region'] = 'eastus'
    api_keys['cognitive_services_api'] = config.retrieve_secret('Cognitive-Services-API')
    api_keys['luis_app_id'] = config.retrieve_secret('LUIS-App-ID')
    api_keys['luis_key'] = config.retrieve_secret('LUIS-API')
    api_keys['openai_key'] = config.retrieve_secret('OpenAI-API')
    api_keys['weather_key'] = config.retrieve_secret('Weather-API')
    api_keys['translator_key'] = config.retrieve_secret('Translator-API')
    api_keys['elevenlabs_api_key'] = config.retrieve_secret('Elevenlabs-API-Key')
    return api_keys