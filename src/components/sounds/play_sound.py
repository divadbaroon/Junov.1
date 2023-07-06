from playsound import playsound
import os

def play_bot_sound(sound_name):
	"""Plays a sound if it exists within the 'sounds' sub directory"""
	
	# Get path to wav file 
	current_directory = os.path.dirname(os.path.abspath(__file__))
	sound_path = os.path.join(current_directory, 'sounds', f'{sound_name}.wav')
 
	# Play sound if it exists
	if os.path.isfile(sound_path):
		playsound(sound_path)
	else:
		print(f"{sound_name}.wav not found. Ensure {sound_name}.wav is located within the 'sounds' directory")