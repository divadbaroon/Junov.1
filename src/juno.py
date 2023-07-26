from src.initialization.initializer import BotInitializer

class Juno:
	"""
 	A simple interface for creating an intelligent and interactive agent.
  
	Params: (all params are optional)
  
	Basic Info:
    - name (str): Name of the agent.
    - role (str): Role of the agent (e.g. virtual assistant, customer, employee, etc.)
    - gender (str): Gender of the agent.
    - language (str): Language of the agent.

    Personality Settings:
    - personality (str): Personality of the agent.
    - prompt (str): Prompt that GPT-3.5-Turbo will use to generate a response.

    Saving Settings:
    - unique (bool): If True, the agent will have its own settings file.
    - save (bool): If false, the agent's settings will not be saved after the program is terminated.

    Voice Settings:
    - voice_engine (str): Voice engine to be used for text-to-speech (currently only supports 'azure' or 'elevenlabs').
    - voice_name (str): Name of the voice to be used for text-to-speech.

    Other Settings:
    - package (str): Package of the agent (only package currently supported is 'virtual assistant').
    - max_response_time (int): Maximum time (in seconds) the agent should take to formulate a response.
  	"""
 
	def __init__(self, **kwargs):
		self._initalize(**kwargs)
  
	def _initalize(self, **kwargs) -> None:
		"""
		Initializes the speech recognition, speech processing, and speech verbalization
		"""	
		self.BotInitializer = BotInitializer(**kwargs)
		self.speech_recognition = self.BotInitializer.speech_recognition
		self.speech_processor = self.BotInitializer.speech_processor
		self.speech_verbalizer = self.BotInitializer.speech_verbalizer
	
	def listen(self) -> str:
		"""
		Listens for users speech input
		:return: (str) speech input
		"""		
		return self.speech_recognition.listen()

	def process(self, speech: str) -> str:
		"""
		Processes and produces a response to users speech
		:param speech: (str) speech input
		:return: (str) response to users speech
		"""
		return self.speech_processor.process_speech(speech)
	
	def verbalize(self, response: str) -> str:
		"""
		Verbalizes a string
		:param response: (str) string to be verbalized
		"""
		self.speech_verbalizer.verbalize_speech(response)
  
	def run(self) -> str:
		"""
		Performs all of bot's functionalities continuously, running indefinitely:
		:.listen() # Listens for users speech
		:.process() # Processes and produces a response to users speech
		:.verbalize() # Verbalizes the response
		"""
		while True:
			speech = self.listen()
			response = self.process(speech)
			self.verbalize(response)
  
