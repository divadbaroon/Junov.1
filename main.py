'''
Note:
The following files must all be located within the same folder for the bot to function.
< pibot.py, speech_recognizer.py, speech_processor.py, speech_verbalizer.py, sample_config.py,  
  bot_properties.json, conversation_history.json >
'''
from pibot import PiBot

def main(persona, gender, language):
  
  # create an instance of pibot with optional parameters
  new_bot = PiBot(persona, gender, language)

  # the bot will continuously listen for input, process it, and produce a response
  # exit the program by saying a generic exit command such as: 'exit', 'quit', 'terminate', or 'end conversation'
  while True:
    # listen for user input
    speech = new_bot.listen()
    # process and produce a response to user input
    response = new_bot.process(speech)
    # verbalize the response
    new_bot.verbalize(response)

    # or run all methods at once
    # new_bot.run()

if __name__ == '__main__':
  personalization_choice = input('Would you like to personalize your bot? (Y/N): ')
  if personalization_choice.lower() == 'y' or personalization_choice.lower() == 'yes':
    persona = input("Enter the persona the bot will embody: ")
    gender = input("Enter the gender of the bot: ")
    language = input("Enter the language the bot will speak (see bot_properties.json to see available languages): ")
    main(persona, gender, language)
  else:
    main('bot', 'female', 'default')