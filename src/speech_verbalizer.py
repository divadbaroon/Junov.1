import sys
import os

# Get the current script's directory and its parent directory
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
if parent_directory not in sys.path:
	sys.path.append(parent_directory)
	
from configuration.bot_properties import BotProperties
import azure.cognitiveservices.speech as speechsdk
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
 
	def __init__(self, audio_config, speech_config, speech_synthesizer):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.bot_properties = BotProperties()
		self.audio_config = audio_config
		self.speech_config = speech_config
		self.speech_synthesizer = speech_synthesizer
		self.reset_language = False
		self.previous_language = None

	def verbalize_speech(self, speech: str):
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
				
				# If the bot is translating, changing the gender, or changing the language the speech will be a dictionary.
				# This is so that the config can be reinitalized with the new property.
				if isinstance(speech, dict):
					if next(iter(speech.keys())) == 'temporary_language':
						
						# One shot translation, thus language is reset to previous language after translation
						self.previous_language = self.bot_properties.retrieve_property('language')
						self.reset_language = True
	  
						self.bot_properties.save_property('language', speech['temporary_language'])
						speech = speech['translated_speech']
	  
					elif next(iter(speech.keys())) == 'gender':
						self.bot_properties.save_property('gender', speech['gender'])
						speech = speech['speech']
	  
					elif next(iter(speech.keys())) == 'language':
						self.bot_properties.save_property('language', speech['language'])
						speech = speech['speech']
					
					# Retrieve the bot's new voice name from bot_properties.json
					voice_name = self.bot_properties.retrieve_property('voice_name')

					# Check if voice with given parameters exists
					if voice_name:
		 
						# Reinitializing the bot's speech config with the new voice name
						self.speech_config.speech_synthesis_voice_name = voice_name
	  
						# Reinitializing the bot's speech synthesizer
						self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
      
				change_language_status = self.bot_properties.retrieve_property('language_changed')
    
				if change_language_status:

					if voice_name:
		 
						# Reinitializing the bot's speech config with the new voice name
						self.speech_config.speech_synthesis_voice_name = voice_name
	  
						# Reinitializing the bot's speech synthesizer
						self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
     
				print('\nResponse:')
				print(f'{persona.title()}: {speech}')

				# Verbalize the given speech
				self.speech_synthesizer.speak_text(speech)
	
				# Resets the language to the previous language if the bot was translating
				if self.reset_language:
					
					self.bot_properties.save_property('language', self.previous_language)

					# Retrieve the bot's new voice name from bot_properties.json
					voice_name = self.bot_properties.retrieve_property('voice_name')

					# Check if voice with given parameters exists
					if voice_name:
		 
						# Reinitializing the bot's speech config with the new voice name
						self.speech_config.speech_synthesis_voice_name = voice_name
	  
						# Reinitializing the bot's speech synthesizer
						self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
	  
					# Set the reset_language flag back to False
					self.reset_language = False
					
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
	
	
   
	


