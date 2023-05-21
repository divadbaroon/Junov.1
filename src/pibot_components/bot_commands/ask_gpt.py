import requests
import json
import webbrowser

class AskGPT:
	"""
	A class that creates a response using OpenAI's GPT-3 API.
	A personalize response is created depening on the user's specified persona and
	the past conversation history to provie context to the conversation.
		
	Atributes:
	language_model (str): language model used for GPT-3 
	response_length (int): max response length of GPT-3's responses
	openai.api_key (str): subscription key for OpenAi's GPT-3
	persona (str): the bot's persona
	"""
			
	def __init__(self):
		self.language_model = "gpt-3.5-turbo"
		self.response_length = 100

	def ask_GPT(self, speech:str, conversation_history:list, openai_key:str, persona:str, language:str, manual_request:str=None,):
		"""
		Uses the user's speech, the bot's persona, and the conversation history 
		to create a response using OpenAI's GPT-3.5-turbo model API.
		:param speech: (str) speech input
		:param conversation_history: (list) the conversation history between the user and the bot
		"""
  
		formatted_conversation_history = self._format_conversation_history(conversation_history)

		# For if I need to manually request a response from GPT-3.5-turbo
		if manual_request:
			prompt = self._construct_manual_prompt(formatted_conversation_history, persona, speech, manual_request=manual_request)

		# Create the chatbot's response using GPT-3.5-turbo model
		else:
			prompt = self._construct_prompt(formatted_conversation_history, persona, speech, language)
   
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
  
		# clean up some errors that gpt somtimes produces in its output
		bad_repsonses = [f'{persona} said:', f'{persona}:', 'response', 'Response:' 'Chatbot:', 'Chatbot :', 'Chatbot said:', 'Chatbot response:', 'chatbot response:']
		for example in bad_repsonses:
			if response.startswith(example):
				response = response.replace(example, '').strip()
	
		return response

	def _format_conversation_history(self, conversation_history):
		"""
		Formats the conversation history to be used as input for GPT-3.5-turbo model.
		"""
		formatted_conversation_history = []
		
		if conversation_history:
			for conversation in conversation_history:
				formatted_conversation_history.append({"role": "user", "content": conversation['User']})
				for name, text in conversation.items():
					if name != 'User':
						formatted_conversation_history.append({"role": "assistant", "content": f"{name.title()} said: {text}"})
		return formatted_conversation_history


	def _construct_prompt(self, formatted_conversation_history, persona, speech, language):
			"""
			Constructs the prompt for the GPT-3.5-turbo model.
			"""
	
			# Creates a prompt used for GPT-3.5-turbo model based on the user's persona and conversation history
			if persona.lower() != 'chatbot':
				prompt = (f"\nProvide your response given this conversation history: \n{formatted_conversation_history}\nI want you to provide the next response to the user. Respond like you are {persona}: The user said: {speech}. Keep it concise. ")
			else:
				prompt = (f"\nProvide your response given this conversation history: \n{formatted_conversation_history}\nI want you to provide the next response to the user. Respond like you are a chatbot: The user said: {speech}. Keep it concise. ")
		
			prompt += f'Do not preface your response with "{persona} said:" or "{persona}:".'
			prompt += f'Respond in {language}. '
			
			return prompt


	def _construct_manual_prompt(self, formatted_conversation_history, persona, speech, manual_request):
		"""
		Constructs the prompt for the GPT-3.5-turbo model when manually requesting a response.
		"""
		prompt = (f"\nProvide your response given this conversation history: \n{formatted_conversation_history}\nI want you to provide the next response to the user. Respond like you are {persona}: The user said: {speech}. Keep it concise")
		prompt += manual_request
		
		return prompt

	def create_gpt_image(self, image: str, openai_key:str):
		"""
		Creates an image using OpenAI's GPT-3 API.
		"""
	
		# url to OpenAI's GPT-3 API
		url = "https://api.openai.com/v1/images/generations"
	
		# Now using the GPT-3.5-turbo model
		payload = {
			"prompt": image,
			"n": 1,
			}
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {openai_key}"
		}

		# Send the POST request to OpenAI's GPT-3 API
		response = requests.post(url, headers=headers, data=json.dumps(payload))
				
		if response.status_code == 200:
			response_json = json.loads(response.content)

			url = response_json['data'][0]['url']
			webbrowser.open(url)
			return f"Ok, I have created an image of {image}."
		else:
					# If the request fails, return a message to the user
			return "Sorry, I am currently experiencing technical difficulties. Please try again later."
