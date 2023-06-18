from src.components.initializer import BotInitializer

class PiBot:
	"""PiBot is a class that provides a simple interface for creating a virtual assistant.
	Three methods are initialized from the BotInitializer class 
 	for the speech recognition, speech processing, and speech verbalization.
 	As well as a run all method that performs all of the bot's functionalities."""
 
	def __init__(self, role='virtual assistant', gender='female', language='english'):
		self.BotInitializer = BotInitializer(role, gender, language)
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
		return self.speech_processor.process_speech(speech, self.speech_verbalizer)
	
	def verbalize(self, response: str):
		"""
		Verbalizes a string
		:param response: (str) string to be verbalized
		"""
		self.speech_verbalizer.verbalize_speech(response)

	def run_once(self):
		"""
		Peforms all of bot's functionalities including:
		:.listen() # Listens for users speech
		:.process() # Processes and produces a response to users speech
		:.verbalize() # Verbalizes the response
		"""
		speech = self.listen()
		response = self.process(speech)
		self.verbalize(response)

	def run(self):
		"""
		Peforms all of bot's functionalities including:
		:.listen() # Listens for users speech
		:.process() # Processes and produces a response to users speech
		:.verbalize() # Verbalizes the response
		"""
		while True:
			speech = self.listen()
			response = self.process(speech)
			self.verbalize(response)
  