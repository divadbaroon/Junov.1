'''
Note:
The following files must all be located within the same folder for the bot to function.
< pibot.py, speech_recognizer.py, speech_processor.py, speech_verbalizer.py, sample_config.py,  
bot_properties.py, bot_properties.json, conversation_history.json, startup_sound.wav(optional) >
'''
		
from pibot.bot_initializer import PiBot
import configuration.config as config

def main():
	
	# Retrieving the bot's secret values from Azure Key Vault
	pibot_api = config.retrieve_secret('PiBot-API')
	luis_app_id = config.retrieve_secret('Luis-APP-ID')
	luis_key = config.retrieve_secret('Luis-API')
	openai_key = config.retrieve_secret('OpenAI-API')
	weather_key = config.retrieve_secret('Weather-API')
	news_key = config.retrieve_secret('News-API')
	translator_key = config.retrieve_secret('PiBot-Translator-API')
	
	# Create an instance of pibot
	new_bot = PiBot(pibot_api=pibot_api, luis_app_id=luis_app_id, luis_key=luis_key, openai_key=openai_key, weather_key=weather_key, translator_key=translator_key, news_key=news_key)

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