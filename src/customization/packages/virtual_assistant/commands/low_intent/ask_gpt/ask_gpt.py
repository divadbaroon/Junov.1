import requests
import json

class AskGPT:
	"""
	A class that creates a response using a specified OpenAI GPT model.
	A response is created depending on the user's speech, the bot's role, the prompt used,
 	and the conversation history.
	"""
	
	def __init__(self, openai_key:str, setting_objects:dict, bot_name:str='Juno', prompt=None):
		self.openai_key = openai_key
		self.profile_settings = setting_objects['profile_settings']
		self.bot_name = bot_name
		self.model = "gpt-3.5-turbo"

		self.prompt = self.profile_settings.retrieve_property('prompt')
		
		# Loading in the conversation history
		# self.conversation_history = self.master_settings.load_conversation_history()
		self.conversation_history = [{"role": "assistant", "content": self.prompt}]

	def ask_GPT(self, speech:str, model=None, manual_request=False) -> str:
		"""
		Uses the user's speech, the bot's role, and the conversation history 
		to create a response using OpenAI's GPT model.
		"""
		# check if model needs to be updated
		if model:
			self.model = model
  
		# get response from gpt
		response = self._send_gpt_request(self.openai_key, speech, manual_request)
		# cleanup response
		response = self._clean_response(response, self.bot_name)
	
		return response

	def _send_gpt_request(self, openai_key:str, speech:str, manual_request=False) -> str:
		"""
		Sends a POST request to the GPT model and returns the response.
		"""
		if manual_request:
			message = [{"role": "user", "content": speech}] 
		else:
			self._update_conversation("user", speech)
			message = self.conversation_history
  
		# url to the GPT model
		url = "https://api.openai.com/v1/chat/completions"

		# Now using the GPT model
		payload = {
			"model": self.model,
			"messages": message,
			"max_tokens": 100,
    		"top_p": 1
		}
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {openai_key}"
		}

		# Send the POST request to the GPT model
		request = requests.post(url, headers=headers, data=json.dumps(payload))
		if request.status_code == 200:
			content = request.json()
		else:
			# print error message
			print(request.text)
			# If the request fails, return a message to the user
			return "Sorry, I am currently experiencing technical difficulties. Please try again later."

		# Extract the 'content' value from the response
		# This is the response from the GPT model
		response = content['choices'][0]['message']['content']
		response = response.strip()
  
		return response 

	def _update_conversation(self, role:str, content:str) -> None:
		"""Updates the conversation history with the user's speech and the bot's response."""
		self.conversation_history.append({"role": role, "content": content})
  
	def _update_prompt(self, prompt:str) -> None:
		"""Updates the prompt to be used for the GPT model."""
		self.prompt = prompt
  
	def _clean_response(self, response:str, bot_name:str) -> str:
		"""Sometimes the response from the GPT model will incorrectly include the bot's name in the response."""
  
		bad_inputs = [f'{bot_name} said: ', f' {bot_name} said: ']
		for example in bad_inputs:
			if example.startswith(response):
				response = response.replace(example, '')
		return response.strip()
			
