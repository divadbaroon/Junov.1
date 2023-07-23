import string
import pyperclip
from random import choice
from src.components.settings.command_settings.command_settings_manager import BotCommandManager

class PasswordGenerator:
	"""
	A class that generates a random password and copies it to the users clipboard.
	"""
 
	def __init__(self):
		self.command_manager = BotCommandManager()
		self.copy_to_clipboard = self.command_manager.retrieve_property(command='password_generator', setting='copy_to_clipboard"')
			
	def generate_password(self, length_of_password: int = 16) -> str:
		"""
		Generates a random password of the specified length and copies it to the users clipboard.
		"""
		password = ''
		# Generate random password
		for _ in range(length_of_password):
			password += choice(string.ascii_letters + string.digits + string.punctuation)
	
		if self.copy_to_clipboard:
			# Copy password
			pyperclip.copy(password)
			return 'A random password has been created and copied to your clipboard.'
		else:
			return 'A random password has been created.'
   
   