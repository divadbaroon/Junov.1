from elevenlabs import generate, play, set_api_key

class ElevenlabsTextToSpeech:
  """
  A class that utilizes Elevenlabs' API to verbalize the bot's response.
  """
  def __init__(self, api_keys:dict, bot_settings):
    set_api_key(api_keys['elevenlabs_api_key'])
    self.voice_name = bot_settings.retrieve_bot_property('current_elevenlabs_voice_name')
  
  def text_to_speech(self, speech:str):
    """Peforms text-to-speech using Elevenlabs' API."""
    audio = generate(
      text=speech,
      voice=self.voice_name,
      model='eleven_multilingual_v1'
    )

    play(audio)
    
  def update_voice(self, new_voice_name:str):
    """Updates the voice name used for Elevenlabs' API."""
    self.voice_name = new_voice_name
