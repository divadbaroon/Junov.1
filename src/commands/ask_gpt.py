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

	def ask_GPT(self, speech:str, conversation_history:list, openai_key:str, persona:str):
		"""
		Uses the user's speech, the bot's persona, and the conversation history 
		to create a response using OpenAI's GPT-3.5-turbo model API.
		:param speech: (str) speech input
		:param conversation_history: (list) the conversation history between the user and the bot
		"""

		formatted_conversation_history = ""
			
		# Formats conversation history to be used as prompt for GPT-3.5-turbo model 
		if conversation_history:
			for conversation in conversation_history:
				formatted_conversation_history += f"User said: {conversation['User']}\n"
				for name, text in conversation.items():
					if name != 'User':
						formatted_conversation_history += f"{name.title()} said: {text}\n"
	
		# Creates a prompt used for GPT-3.5-turbo model based on the user's persona and conversation history
		if persona != 'chatbot' and formatted_conversation_history:
			prompt = (f"\nProvide your response given this conversation history: \n{formatted_conversation_history}\nI want you to provide the next response to the user. Respond like you are {self.persona}: The user said: {speech}. Keep it concise")
		elif persona == 'chatbot' and formatted_conversation_history:
			prompt = (f"\nProvide your response given this conversation history: \n{formatted_conversation_history}\nProvide a chatbot like response to the next user input and do not provide 'chatbot response' in the response: The user said: {speech}. Keep it concise")
		elif persona != 'chatbot' and not formatted_conversation_history:
			prompt = (f"\nI want you to respond to the user like you are {persona}. The user said: {speech}. Keep it concise")
		else:
			prompt = (f"\nProvide a chatbot like response to the user: The user said: {speech}. Keep it concise")
				
		# url to OpenAI's GPT-3 API
		url = "https://api.openai.com/v1/chat/completions"
	
		# Now using the GPT-3.5-turbo model
		payload = {
			"model": "gpt-3.5-turbo",
			"messages": [{"role": "assistant", "content": prompt}]
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
		bad_repsonses = [f'{persona} said:', f'{persona}:', 'response', 'Chatbot:', 'Chatbot :', 'Chatbot said:', 'Chatbot response:', 'chatbot response:']
		for example in bad_repsonses:
			if response.startswith(example):
				response = response.replace(example, '').strip()
	
		return response

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