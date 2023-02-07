'''
Note:
The following files must all be located within the same folder for the bot to function.
< pibot.py, speech_recognizer.py, speech_processor.py, speech_verbalizer.py, sample_config.py,  
  bot_properties.json, conversation_history.json >  
'''

from speech_recognizer import SpeechRecognition
from speech_processor import SpeechProcessor
from speech_verbalizer import SpeechVerbalizer

class PiBot:
  '''
  PiBot is a class that provides a simple interface for creating a chatbot.
  It uses three classes for the speech recognition, speech processing, and speech verbalization.
 
  Attributes:
  persona (str): name of person the bot will emobdy
  gender (str): the gender of the bot
  langauge (str): the language the bot will speak
  speech_recognition: object of SpeechRecognition class
  speech_processor: object of SpeechProcessor class
  speech_verbalizer: object of SpeechVerbalizer class
  '''
  
  def __init__(self, persona='bot', gender='female', language='default'):
    """
    Initializes a new PiBot object 
    :param persona: (str) name of person the bot will emobdy
    :param gender: (str) the gender of the bot
    :param language: (str) the language the bot will speak
    """
    self.persona = persona
    self.gender = gender
    self.language = language
    self.speech_recognition = SpeechRecognition()
    self.speech_processor = SpeechProcessor()
    self.speech_verbalizer  = SpeechVerbalizer()
  
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
    return self.speech_processor.process_speech(speech, self.persona, self.gender, self.language)

  def verbalize(self, response: str):
    """
    Verbalizes a string
    :param response: (str) string to be verbalized
    """
    self.speech_verbalizer.verbalize_speech(response, self.persona, self.gender, self.language)
  
  def run(self):
    """
    Peforms all of bot's functionalities including:
    :.listen() # Listens for users speech
    :.process() # Processes and produces a response to users speech
    :.verbalize() # Verbalizes the response
    """
    speech = self.speech_recognition.listen()
    response = self.speech_processor.process_speech(speech, self.persona, self.gender, self.language)
    self.speech_verbalizer.verbalize_speech(response, self.persona, self.gender, self.language)
      