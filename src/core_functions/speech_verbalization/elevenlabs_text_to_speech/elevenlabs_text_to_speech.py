from elevenlabs import generate, play, set_api_key

class ElevenlabsTextToSpeech:
  """
  A class that utilizes Elevenlabs' API to verbalize the bot's response.
  """
  def __init__(self, profile_name:str, api_keys:dict, setting_objects:object):
    self.profile_name = profile_name
    set_api_key(api_keys['ELEVENLABS-API-KEY'])
    self.profile_settings = setting_objects['profile_settings']
    self.voice_settings = setting_objects['voice_settings']
    #self.voice_name = self.profile_settings.retrieve_property('voice_name', profile_name=self.profile_name)
  
  def text_to_speech(self, speech:str, language_country_code:str):
    """
    Peforms text-to-speech using Elevenlabs' API.
    """
    voice_name = self.profile_settings.retrieve_property('voice_name', profile_name=self.profile_name)
    voice_code = self.voice_settings.retrieve_custom_voice_id(voice_name)
    audio = generate(
      text=speech,
      voice=voice_code,
      model='eleven_multilingual_v1'
    )

    play(audio)
    
  def update_voice(self):
    """
    Updates the voice name used for Elevenlabs' API.
    """
    self.voice_name =  self.profile_settings.retrieve_property('voice_name', profile_name=self.profile_name)
