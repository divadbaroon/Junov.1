'''
Note:
The following files must all be located within the same folder for the bot to function.
< pibot.py, speech_recognizer.py, speech_processor.py, speech_verbalizer.py, sample_config.py,  
  bot_gender_and_languages.json, bot_mute_status.json >
'''

from pibot import PiBot

# create an instance of pibot with optional parameters
# parameters include:
    # persona - personality the bot will embody
    # gender - gender of the bot
    # language - language the bot will speak
new_bot = PiBot('Barack Obama', 'Male', 'English_USA')

while True:
  # listen for user input
  speech = new_bot.listen()
  # process and produce a response to user input
  response = new_bot.process(speech)
  # verbalize the response
  new_bot.verbalize(response)

# or run all methods at once
new_bot.run()