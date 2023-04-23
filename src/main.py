'''
Note:
The following files must all be located within the same folder for the bot to function.
< pibot.py, speech_recognizer.py, speech_processor.py, speech_verbalizer.py, sample_config.py,  
  bot_properties.py, bot_properties.json, conversation_history.json, startup_sound.wav(optional) >
'''

from pibot import PiBot

def main(persona, gender, language):
  
  # Create an instance of pibot with optional parameters
  new_bot = PiBot(persona, gender, language)

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
    main(persona='Chatbot', gender='Female', language='english_usa')