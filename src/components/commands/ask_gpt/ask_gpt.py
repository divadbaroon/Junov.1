import requests
import json

class AskGPT:
	"""
	A class that creates a response using OpenAI's GPT-3.5-turbo model API.
	A rolelize response is created depening on the user's specified role and
	the past conversation history to provie context to the conversation.
		
	Atributes:
	openai_key (str): subscription key for OpenAi's GPT-3
	"""
	
	def __init__(self, openai_key:str, bot_settings:object, bot_name:str, prompt=None):
		self.openai_key = openai_key
		self.bot_settings = bot_settings
		self.bot_name = bot_name
  
		self.model = "gpt-3.5-turbo"

		# Construct the prompt model 
		if prompt:
			self.prompt = prompt
		else:
			self.prompt =  f"You are a helpful virtual assistant named {bot_name}. Keep your responses concise yet informative to the user."
   
		# Loading in the conversation history
		# self.conversation_history = self.bot_settings.load_conversation_history()
		self.conversation_history = [{"role": "assistant", "content": self.prompt}]

	def ask_GPT(self, speech:str, model=None, manual_request=False) -> str:
		"""
		Uses the user's speech, the bot's role, and the conversation history 
		to create a response using OpenAI's GPT-3.5-turbo model API.
		:param speech: (str) speech input
  
		:return response: (str) response from GPT-3.5-turbo model 
		"""
		# check if model needs to be updated
		if model:
			self.model = model
  
		# get response from gpt
		response = self._send_gpt_request(self.openai_key, speech, manual_request)
		# cleanup response
		response = self._clean_response(response, self.bot_name)
	
		return response

	def _update_conversation(self, role:str, content:str) -> None:
		self.conversation_history.append({"role": role, "content": content})
  
	def _update_prompt(self, prompt:str) -> None:
		self.prompt = prompt

	def _send_gpt_request(self, openai_key:str, speech:str, manual_request=False) -> str:
		"""
		Sends a POST request to the OpenAI's GPT-3.5-turbo API and returns the response.
		:param openai_key: (str) the API key for OpenAI's GPT-3.5-turbo
		:param speech: (str) speech input

		:return response: (str) the response from GPT-3.5-turbo, or an error message if the request fails
		"""
		if manual_request:
			message = [{"role": "user", "content": speech}] 
		else:
			self._update_conversation("user", speech)
			message = self.conversation_history
  
		# url to OpenAI's GPT-3 API
		url = "https://api.openai.com/v1/chat/completions"

		# Now using the GPT-3.5-turbo model
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

		# Send the POST request to OpenAI's GPT-3 API
		request = requests.post(url, headers=headers, data=json.dumps(payload))
		if request.status_code == 200:
			content = request.json()
		else:
			# print error message
			print(request.text)
			# If the request fails, return a message to the user
			return "Sorry, I am currently experiencing technical difficulties. Please try again later."

		# Extract the 'content' value from the response
		# This is the response from the GPT-3.5-turbo model
		response = content['choices'][0]['message']['content']
		response = response.strip()
  
		return response 

	def _clean_response(self, response:str, bot_name:str) -> str:
		"""Sometimes the response from GPT-3.5-turbo model will incorrectly include the bot's name in the response."""
  
		bad_inputs = [f'{bot_name} said: ', f' {bot_name} said: ']
		for example in bad_inputs:
			if example.startswith(response):
				response = response.replace(example, '')
		return response.strip()
			
