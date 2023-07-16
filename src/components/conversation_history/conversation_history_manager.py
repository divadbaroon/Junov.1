import json
import os

# Construct the path to the conversation_history.json file in the 'conversation_history' folder
current_directory = os.path.dirname(os.path.abspath(__file__))
conversation_history_path = os.path.join(current_directory, 'conversation_history.json')

class ConversationHistoryManager:
	"""
	A class that manages the conversation history in the file "conversation_history.json".
	"""

	def load_conversation_history(self) -> list:
		"""
		Loads the conversation history from the conversation_history.json file
		:return: (list) the conversation history
		"""
		try:
			with open(conversation_history_path, 'r', encoding='utf-8') as f:
				data = json.load(f)
				conversation_history = data["conversation"]
		except FileNotFoundError:
			print('The file "conversation_history.json" is missing.\nMake sure all files are located within the same folder')

		return conversation_history

	def get_conversation_history(self, role: str):
		"""
		Gets the conversation history from the conversation_history.json file
		and prints it to the console
		:return: (str) the conversation history
		"""
		# load conversation history from conversation_history.json file
		conversation_history = self.load_conversation_history()
		formatted_conversation_history = ""

		# Reformat conversation history to make it more readable
		if conversation_history:
			for conversation in conversation_history:
				formatted_conversation_history += f"Input: \nUser: {conversation['User']}\n\n"
				formatted_conversation_history += f"Response: \n{role}: {conversation[role]}\n\n"

		print(f'\nConversation History: \n{formatted_conversation_history}')
		return 'Ok, I have printed the conversation history to the console'
				
	def save_conversation_history(self, speech: str, response: str, role: str, bot_name:str):
		"""
		Saves the new conversation along with the rest of the conversation
		history to conversation_history.json file
		:param speech: (str) the user's speech
		:param response: (str) the bot's response
		"""
		# load conversation history from conversation_history.json file
		conversation_history = self.load_conversation_history()

		# Add new conversation to the conversation history
		new_conversation = {
		"User": speech,
		bot_name.title(): response
		}
		conversation_history.append(new_conversation)
		data = {"conversation": conversation_history}
		try:
			with open(conversation_history_path, "w", encoding="utf-8") as f:
				json.dump(data, f, ensure_ascii=False, indent=4)
		except FileNotFoundError:
			print('The file "conversation_history.json" is missing.Make sure all files are located within the same folder')

	def clear_conversation_history(self):
		"""
		Clears the conversation history
		"""
		# Reset the contents of conversation_history.json
		with open(conversation_history_path, "w") as file:
			json.dump({"conversation": []}, file)
		return 'Ok, I have cleared the conversation history'
						
	def exit_and_clear_conversation_history(self):
		"""
		Clears the conversation history and exits the program
		"""
		# Reset the contents of conversation_history.json	
		with open(conversation_history_path, "w") as file:
			json.dump({"conversation": []}, file)

		# verbalize a response before exiting the program
		return 'Exiting. Goodbye!'