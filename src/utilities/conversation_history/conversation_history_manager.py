import yaml
from datetime import datetime, date
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager
from customization.profiles.profile_manager import ProfileManager

class ConversationHistoryManager:
	"""A class that manages the conversation history in the file "conversation_history.yaml"."""
	
	def __init__(self):
		self.profile_name = MasterSettingsManager().retrieve_property('profile')
		self.entity_name = ProfileManager().retrieve_property('name', self.profile_name)
		self.conversation_history_path = f'src/profiles/profile_storage/{self.profile_name}/conversation_history.yaml'
		self.new_session = True
		
	def setup_new_session(self):
		"""Sets up a new session by clearing the conversation history"""
		data = self.load_conversation_history()
		current_session_number = self._retrieve_past_session_number() + 1
		data[f'Session {current_session_number}'] = {
			'Date': date.today().strftime("%d/%m/%Y"),
			'Time': datetime.now().strftime("%H:%M:%S"),
			'Conversation': []
		}
		self._save_data_to_file(data)

	def _retrieve_past_session_number(self):
		"""Gets the current session number"""
		data = self.load_conversation_history()
		# Get all keys that start with "Session", extract their numbers, then get the maximum
		session_numbers = [int(key.split()[1]) for key in data.keys() if key.startswith("Session")]
		return max(session_numbers, default=0)

	def load_conversation_history(self) -> dict:
		"""Loads the conversation history from the conversation_history.yaml file"""
		try:
			with open(self.conversation_history_path, 'r', encoding='utf-8') as f:
				data = yaml.safe_load(f) or {}
		except FileNotFoundError:
			print('The file "conversation_history.yaml" is missing.\nMake sure all files are located within the same folder.')
			data = {}
		return data

	def save_conversation_history(self, speech: str, response: str):
		"""Saves the new conversation along with the rest of the conversation history to conversation_history.yaml file"""
		if self.new_session:
			self.setup_new_session()
			self.new_session = False

		data = self.load_conversation_history()
		current_session_key = f"Session {self._retrieve_past_session_number()}"
		conversation_entry = {
			"User": speech,
			f"{self.entity_name.title()}": response
		}
		if "Conversation" not in data[current_session_key]:
			data[current_session_key]["Conversation"] = []
		data[current_session_key]['Conversation'].append(conversation_entry)
		self._save_data_to_file(data)

	def _save_data_to_file(self, data):
		"""Saves the conversation history to conversation_history.yaml file"""
		try:
			with open(self.conversation_history_path, "w", encoding="utf-8") as f:
				yaml.safe_dump(data, f)
		except FileNotFoundError:
			print('The file "conversation_history.yaml" is missing. Make sure all files are located within the same folder.')

	def clear_conversation_history(self):
		"""Clears the conversation history"""
		try:
			with open(self.conversation_history_path, "w") as file:
				yaml.safe_dump({"conversation": []}, file)
		except FileNotFoundError:
			print('The file "conversation_history.yaml" is missing. Make sure all files are located within the same folder.')
		return 'Ok, I have cleared the conversation history'

	def exit_and_clear_conversation_history(self):
		"""Clears the conversation history and exits the program"""
		self.clear_conversation_history()
		return 'Exiting. Goodbye!'

