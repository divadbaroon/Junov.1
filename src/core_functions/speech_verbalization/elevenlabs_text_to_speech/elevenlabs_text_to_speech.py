from elevenlabs import generate, play, set_api_key, voices
from configuration.manage_secrets import ConfigurationManager

class ElevenlabsTextToSpeech:
  """
  A class that utilizes Elevenlabs' API to verbalize the bot's response.
  """
  def __init__(self, profile_name:str, api_keys:dict, setting_objects:object):
    self.configuration_manager = ConfigurationManager()
    self.api_keys = api_keys
    self.elevenlabs_key = api_keys['ELEVENLABS-API-KEY']
    set_api_key(self.elevenlabs_key )
    self.profile_name = profile_name
    self.profile_settings = setting_objects['profile_settings']
    self.voice_settings = setting_objects['voice_settings']
    self.voice_name = self.profile_settings.retrieve_property('voice_name', profile_name=self.profile_name)
  
  def text_to_speech(self, speech:str, language_country_code:str):
    """
    Peforms text-to-speech using Elevenlabs' API.
    """
    self.voice_name = self.profile_settings.retrieve_property('voice_name', profile_name=self.profile_name)
    voice_code = self.api_keys[self.voice_name.title()]
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
    