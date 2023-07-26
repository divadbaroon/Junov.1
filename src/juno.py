from src.initialization.initializer import BotInitializer

class Juno:
	"""
	A simple interface for creating an intelligent and interactive agent.
  
	Params: 
		Basic Info:
		- name (str, default='Juno'): Name of the agent.
		- role (str, default='assistant'): Role of the agent.
		- gender (str, default='female'): Gender of the agent.
		- language (str, default='english'): Language of the agent.
		
		Personality Settings:
		- personality (str, default='friendly'): Personality of the agent.
		- prompt (str, default=''): Prompt for GPT to generate a response.
		- gpt_model (str, default='GPT-3.5-Trubo'): GPT model for generating responses.
		
		Saving Settings:
		- unique (bool, default=False): If True, agent will have its own settings file.
		- save (bool, default=True): If False, agent's settings won't be saved post termination.
		
		Voice Settings:
		- voice_engine (str, default='azure'): Voice engine for text-to-speech.
		- voice_name (str, default='Amber'): Voice name for text-to-speech.
		
		Other Settings:
		- package (str, default=None): Package of the agent.
		- max_response_time (int): Maximum response time in seconds.
		- startup_sound (bool, default=True): If True, bot plays a startup sound on initialization.
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
  
