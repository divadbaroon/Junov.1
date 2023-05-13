'''
Note:
The following files must all be located within the same folder for the bot to function.
< pibot.py, speech_recognizer.py, speech_processor.py, speech_verbalizer.py, sample_config.py,  
bot_properties.py, bot_properties.json, conversation_history.json, startup_sound.wav(optional) >
'''
		
from pibot.bot_initializer import PiBot
import configuration.secrets.config as config

def main():
	
	# Retrieving the bot's secret values from Azure Key Vault
	cognitive_services_api = config.retrieve_secret('Cognitive-Services-API')
	clu_key = config.retrieve_secret('CLU-Key')
	clu_endpoint = config.retrieve_secret('CLU-Endpoint')
	clu_project_name = config.retrieve_secret('CLU-Poject-Name')
	clu_deployment_name = config.retrieve_secret('CLU-Deployment-Name')
	openai_key = config.retrieve_secret('OpenAI-API')
	weather_key = config.retrieve_secret('Weather-API')
	news_key = config.retrieve_secret('News-API')
	translator_key = config.retrieve_secret('Translator-API')
 
	# The region must match the region of the cognitive services resource
	region = 'eastus'
	
	# Create an instance of pibot
	new_bot = PiBot(cognitive_services_api=cognitive_services_api, region=region, clu_endpoint=clu_endpoint, clu_project_name=clu_project_name, clu_deployment_name=clu_deployment_name, clu_key=clu_key, openai_key=openai_key, weather_key=weather_key, translator_key=translator_key, news_key=news_key)

	# The bot will continuously listen for input, process it, and produce a response
	# Exit the program by saying a generic exit command such as: 'exit', 'quit', 'terminate', or 'end conversation'
	while True:
		# Listen for user input
		speech = new_bot.listen()
		# Process and produce a response to user input
		response = new_bot.process(speech)
		# Verbalize the response
		new_bot.verbalize(response)

		# Or run all methods at once
		# new_bot.run()      
		
if __name__ == '__main__':
		main()