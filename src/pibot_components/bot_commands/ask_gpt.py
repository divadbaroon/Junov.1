import requests
import json

class AskGPT:
	"""
	A class that creates a response using OpenAI's GPT-3.5-turbo model API.
	A personalize response is created depening on the user's specified persona and
	the past conversation history to provie context to the conversation.
		
	Atributes:
	openai_key (str): subscription key for OpenAi's GPT-3
	"""
	
	def __init__(self, openai_key:str):
		self.openai_key = openai_key

	def ask_GPT(self, speech:str, conversation_history:list, persona:str, bot_name:str, language:str, manual_request:str=None) -> str:
		"""
		Uses the user's speech, the bot's persona, and the conversation history 
		to create a response using OpenAI's GPT-3.5-turbo model API.
		:param speech: (str) speech input
		:param conversation_history: (list) the conversation history between the user and the bot
		:param persona: (str) the bot's persona
		:param language: (str) the language in which the response should be given
		:param manual_request: (str) optional manual request string
  
		:return response: (str) response from GPT-3.5-turbo model 
		"""
  
		# Format the conversation history to be used as context for GPT-3.5-turbo model
		formatted_conversation_history = self._format_conversation_history(conversation_history)

		# Manual requests are used if I want a customized response from GPT-3.5-turbo for special cases
		if manual_request:
			prompt = self._construct_manual_prompt(formatted_conversation_history, persona, speech, manual_request=manual_request)
		# Create the virtual assistant's response using GPT-3.5-turbo model
		else:
			prompt = self._construct_prompt(formatted_conversation_history, persona, bot_name, speech, language)

		# Send a POST request to OpenAI's GPT-3 API
		response = self._send_gpt_request(formatted_conversation_history, self.openai_key, prompt)
  
		response = self._clean_response(response, bot_name)
	
		return response

	def _format_conversation_history(self, conversation_history) -> list:
		"""
		Formats the conversation history to be used as input for the GPT-3.5-turbo model.
		:param conversation_history: (list) a list of dictionaries representing the conversation history. 
									Each dictionary contains 'User' as a key representing user's message and 
									other keys representing assistant's messages.

		:return formatted_conversation_history: (list) a list of dictionaries formatted for GPT-3.5-turbo.
		"""
  
		formatted_conversation_history = []
		
		if conversation_history:
			for conversation in conversation_history:
				formatted_conversation_history.append({"role": "user", "content": conversation['User']})
				for name, text in conversation.items():
					if name != 'User':
						formatted_conversation_history.append({"role": "assistant", "content": f"{name.title()} said: {text}"})
		return formatted_conversation_history

	def _construct_prompt(self, formatted_conversation_history, persona, bot_name, speech, language) -> str:
		"""
		Constructs the prompt for the GPT-3.5-turbo model based on the conversation history, the persona, and the user's speech.
		:param formatted_conversation_history: (list) a list of formatted conversation history messages
		:param persona: (str) the bot's persona
		:param speech: (str) the last user's speech/input
		:param language: (str) the language in which the response should be given

		:return prompt: (str) the constructed prompt for GPT-3.5-turbo
		"""

		# Creates a prompt used for GPT-3.5-turbo model based on the user's persona and conversation history
		if persona.lower() != 'virtual assistant':
			prompt = (f'\nProvide your response given this conversation history: \n{formatted_conversation_history}\nI want you to provide the next response to the user. Respond like you are {persona}: The user said: "{speech}". Keep it concise.' )
		else:
			prompt = (f'\nProvide your response given this conversation history: \n{formatted_conversation_history}\nI want you to provide the next response to the user. Respond like you are a virtual assistant: The user said: "{speech}". Keep it concise. ')
	
		prompt += f' \nRespond in {language}. '
  
		print(prompt)
			
		return prompt

	def _construct_manual_prompt(self, formatted_conversation_history, persona, speech, manual_request) -> str:
		"""
		Constructs the prompt for the GPT-3.5-turbo model when manually requesting a response.
		:param formatted_conversation_history: (list) formatted conversation history
		:param persona: (str) the bot's persona
		:param speech: (str) speech input
		:param manual_request: (str) additional specific instructions or queries to GPT-3
  
		:return prompt: (str) the constructed prompt
		"""
		prompt = (f"\nProvide your response given this conversation history: \n{formatted_conversation_history}\nI want you to provide the next response to the user. Respond like you are {persona}: The user said: {speech}. Keep it concise")
		prompt += manual_request
		
		return prompt

	def _send_gpt_request(self, formatted_conversation_history, openai_key, prompt) -> str:
		"""
		Sends a POST request to the OpenAI's GPT-3.5-turbo API and returns the response.
		:param formatted_conversation_history: (list) a list of formatted conversation history messages
		:param openai_key: (str) the API key for OpenAI's GPT-3.5-turbo
		:param prompt: (str) the constructed prompt for GPT-3.5-turbo

		:return response: (str) the response from GPT-3.5-turbo, or an error message if the request fails
		"""
     
		# url to OpenAI's GPT-3 API
		url = "https://api.openai.com/v1/chat/completions"
	
		# Now using the GPT-3.5-turbo model
		payload = {
			"model": "gpt-3.5-turbo",
			"messages": formatted_conversation_history + [{"role": "user", "content": prompt}]
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
			# If the request fails, return a message to the user
			return "Sorry, I am currently experiencing technical difficulties. Please try again later."

		# Extract the 'content' value from the response
		# This is the response from the GPT-3.5-turbo model
		response = content['choices'][0]['message']['content']
		response = response.strip()
  
		return response 

	def _clean_response(self, response, bot_name) -> str:
		"""Sometimes the response from GPT-3.5-turbo model will incorrectly include the bot's name in the response."""
  
		bad_inputs = [f'{bot_name.title()} said:']
		for example in bad_inputs:
			if example.startswith(response):
				response = response.replace(example, '')
		return response.strip()
			
