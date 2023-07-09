import json
import os

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the bot_settings.json file in the 'voice' folder
command_settings_path = os.path.join(current_directory, 'command_settings.json')

class BotCommandManager:
	"""
	A class that can retrieve and save properties to "command_settings.json".
	"""
	def __init__(self):
		self.data = self.load_command_settings()

	def load_command_settings(self) -> dict:
		"""Loads the data from "command_settings.json" and returns it as a dictionary."""
		try:
			with open(command_settings_path, "r") as f:
				return json.load(f)
		except FileNotFoundError:
			print('The file "command_settings.json" is missing.\nMake sure all files are located within the same folder.')
			raise SystemExit()

	def retrieve_property(self, command:str, setting: str) -> str:
		"""Retrieves a property from "command_settings.json" and returns it."""
		
		if command in ['get_weather', 'password_generator']:
			return self.data[command].get(setting)
		
	def retrieve_properties(self) -> dict:
		"""Retrieves all properties from "command_settings.json" and returns them."""
		return self.data

	def save_property(self, command:str, setting: str, value: str) -> None:
		"""Save a property to "command_settings.json."""
		
		if command in ['get_weather', 'password_generator']:
			self.data[command][setting] = value
		
		# write data back
		with open(command_settings_path, "w") as f:
			json.dump(self.data, f, indent=4)

	def reload_settings(self) -> None:
		"""Reloads the data from "command_settings.json" and stores it in self.data."""
		self.data = self.load_command_settings()	