import os
from playsound import playsound

class PlaySound:
    
	def __init__(self) -> None:
		"""Initializes the PlaySound object"""
		self.sound_names = {'start_up_sound': 'startup_sound.wav', 'error_sound': 'error_sound.wav'}

	def _play_sound_if_exists(self, sound):
		"""Plays startup sound if it exists"""
		# If sound is valid, play it
		if sound in self.sound_names:

			# Construct the path to the configuration directory and the conversation_history.json file
			current_directory = os.path.dirname(os.path.abspath(__file__))
			sound_file_path = os.path.join(current_directory, 'sounds', self.sound_names[sound])
			# Normalize the path (remove any redundant components)
			sound_file_path = os.path.normpath(sound_file_path)

			# Plays startup sound if it exists
			if os.path.isfile(sound_file_path):
				playsound(sound_file_path)