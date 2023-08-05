from src.initialization.initializer import BotInitializer
from src.profiles.profile_manager import ProfileManager

class Juno:
	"""
	A simple interface for creating an intelligent and interactive agent.
	"""
 
	def __init__(self, profile_name:str='default'):
		self._initalize(profile_name)
  
	def _initalize(self, profile_name:str) -> None:
		"""
		Initializes the speech recognition, speech processing, and speech verbalization
		"""	
		self.BotInitializer = BotInitializer(profile_name)
		self.speech_recognition = self.BotInitializer.speech_recognition
		self.speech_processor = self.BotInitializer.speech_processor
		self.speech_verbalizer = self.BotInitializer.speech_verbalizer
		self.profile_manager = ProfileManager()
	
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
   
	def create_profile(self, profile:dict) -> None:
		"""
		Adds a profile to the bot
		:param profile: (dict) profile to be added
		"""
		self.profile_manager.create_profile(profile)
  
	def remove_profile(self, profile:dict) -> None:
		"""
		Adds a profile to the bot
		:param profile: (dict) profile to be added
		"""
		self.profile_manager.remove_profile(profile)
  
	def get_profiles(self) -> dict:
		"""
		Gets all profiles
		:return: (dict) all profiles
		"""
		return self.profile_manager.load_profile_data()

	def get_voices(self, engine='azure') -> list:
		"""
		Gets all voices
		:return: (dict) all voices
		"""
		return self.BotInitializer.get_voices(engine=engine)
