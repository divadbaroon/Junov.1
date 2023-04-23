from bot_properties import BotProperties
from performance_logger import performance_logger
import sys
import json 

class SpeechVerbalizer:
	"""
	A class that utilizes Azure's Cognitive Speech Service to verbalize the bot's response.

	Attributes:
	bot_properties (BotProperties): A BotProperties object that contains information about the bot's properties.
	speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
	audio_config (AudioOutputConfig): A configuration object that specifies the use of the default speaker
	speech_synthesizer (SpeechSynthesizer): A synthesizer object that uses the above configurations to generate the spoken words
	"""
 
	def __init__(self):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.bot_properties = BotProperties()

	@performance_logger
	def verbalize_speech(self, speech: str, speech_config, speech_synthesizer):
		"""
		Verbalizes a given string with a specified gender and langauge of voice.
		:param speech (str): The speech to be verbalized.
		"""	

		# Retrieve the bot's mute status and persona from bot_properties.json
		mute_status = self.bot_properties.retrieve_property('mute_status')
		persona = self.bot_properties.retrieve_property('persona')

		# Check if there is speech to verbalize
		if speech:
      
			# Check the bot's mute status
			if not mute_status: 
	   
				# Retrieve the bot's voice name from bot_properties.json
				voice_name = self.bot_properties.retrieve_property('voice_name')

				# Check if voice with given parameters exists
				if voice_name:
					speech_config.speech_synthesis_voice_name = voice_name
				else:
					speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural' # used as a backup 

				print('\nResponse:')
				print(f'{persona.title()}: {speech}')

				# Verbalize the given speech
				speech_synthesizer.speak_text(speech)

				# Check if user wanted to end the program after verbalizing exit speech
				if speech == 'Exiting. Goodbye!':
        
					# Reset the contents of conversation_history.json	
					with open("conversation_history.json", "w") as file:
						json.dump({"conversation": []}, file)
					sys.exit()
			else:
				print('\n(muted) Response:')
				print(f'{persona.title()}: {speech}')
		else:
			print('No speech has been provided to verbalize.')
	
	
   
	


