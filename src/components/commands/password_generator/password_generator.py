import string
import pyperclip
from random import choice

class PasswordGenerator:
	"""
	A class that generates a random password and copies it to the users clipboard.
	"""
			
	def generate_password(self, length: int = 16, copy_to_clipboard: bool = True):
		"""
		Generates a random password of the specified length and copies it to the users clipboard.
		:param length: (int) the length of the password
		:return: (str) a message that a password has been generated and copied to the clipboard
		"""
		password = ''
		# Generate random password
		for _ in range(length):
			password += choice(string.ascii_letters + string.digits + string.punctuation)
	
		if copy_to_clipboard:
			# Copy password
			pyperclip.copy(password)
			return 'A random password has been created and copied to your clipboard.'
		else:
			return 'A random password has been created.'
   
   