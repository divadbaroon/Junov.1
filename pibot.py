'''
-------------------------------------------------------------------------------------------------------
Name: PiBot
Created: 1-8-23
Last modified: 1-30-23
-------------------------------------------------------------------------------------------------------
Description:
PiBot is a class that provides a simple interface for creating a personalized chatbot capable of 
performing commands and providing conversations with users by utilizing OpenAi's chatGPT.
The SpeechRecognition class uses Azure's Cognitive Speech Services for listening to speech input.
the SpeechProcessor class uses Azure's LUIS Service to process the user's input and check for similarity 
between the user's input and the Luis trained model. If minimal similarites are found a response is created using
chatGPT. The SpeechVerbalizer class uses Azure's Cognitive Speech Services for verbalizing the responses.
The bot's gender, language, and current mute status are stored in a .json file.
-------------------------------------------------------------------------------------------------------
Usage:
  # Create an instance of pibot with optional parameters
  new_bot = PiBot('persona', 'gender', 'language') 
          - persona: The persona that the bot will embody
          - gender: The gender of the voice the bot will respond in
          - langauge: The langauge the bot will respond in
                  Currently supported languages include: 
                - Arabic, English_USA, English_UK, English_Australia, English_Ireland
                  Spanish, French, Mandarin, Hindi
    # Bot listens for user's speech
  speech = new_bot.listen() 
  # Bot processes and provides a response to user's speech
  response = new_bot.process(speech) 
  # Bot's response is verbalized
  new_bot.verbalize(response) 
-------------------------------------------------------------------------------------------------------
Note:
The following files must all be located within the same folder for the bot to function properly.
< pibot.py, speech_recognizer.py, speech_processor.py, speech_verbalizer.py, sample_config.py,  
  bot_gender_and_languages.json, bot_mute_status.json >  
-------------------------------------------------------------------------------------------------------
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
    self.speech_verbalizer  = SpeechVerbalizer(self.persona, self.gender, self.language)
  
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
    return self.speech_processor.process_speech(speech, self.persona)

  def verbalize(self, response: str):
    """
    Verbalizes a string
    :param response: (str) string to be verbalized
    """
    self.speech_verbalizer.verbalize_speech(response)
  
  def run(self):
    """
    Peforms all of bot's functionalities including:
    :.listen() # Listens for users speech
    :.process() # Processes and produces a response to users speech
    :.verbalize() # Verbalizes the response
    """
    speech = self.speech_recognition.listen()
    response = self.speech_processor.process_speech(speech, self.persona)
    self.speech_verbalizer.verbalize_speech(response)
      