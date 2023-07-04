from elevenlabs import generate, play, set_api_key

class ElevenlabsTextToSpeech:
  """
  A class that utilizes Elevenlabs' API to verbalize the bot's response.
  """
  def __init__(self, api_keys:dict, bot_settings:object):
    set_api_key(api_keys['elevenlabs_api_key'])
    self.bot_settings = bot_settings
    self.voice_name = self.bot_settings.retrieve_property('voice', 'current_elevenlabs_voice_name')
  
  def text_to_speech(self, speech:str):
    """Peforms text-to-speech using Elevenlabs' API."""
    audio = generate(
      text=speech,
      voice=self.voice_name,
      model='eleven_multilingual_v1'
    )

    play(audio)
    
  def update_voice(self):
    """Updates the voice name used for Elevenlabs' API."""
    self.voice_name = self.bot_settings.retrieve_property('voice', 'current_elevenlabs_voice_name')
