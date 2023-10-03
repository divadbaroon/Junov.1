import openai

class AskGPT:
	"""
	A class that creates a response using a specified OpenAI GPT model.
	A response is created depending on the user's speech, the bot's role, the prompt used,
 	and the conversation history.
	"""
	
	def __init__(self, openai_key:str, setting_objects:dict, bot_name:str='Juno'):
		openai.api_key = openai_key
		self.profile_settings = setting_objects['profile_settings']
		self.bot_name = bot_name
		# fine tuned assistant model
		self.model = "ft:gpt-3.5-turbo-0613:personal:juno-test:7zqjfAto"

		self.prompt = self.profile_settings.retrieve_property('prompt')
		
		# Loading in the conversation history
		# self.conversation_history = self.master_settings.load_conversation_history()
		self.conversation_history = [{"role": "assistant", "content": "You are an assistant capable of answering questions in a friendly and concise manner"}]
		#self.conversation_history = []

	def ask_GPT(self, speech:str, model:str=None, manual_request:bool=False, max_tokens:int=100) -> str:
		"""
		Uses the user's speech, the bot's role, and the conversation history 
		to create a response using OpenAI's GPT model.
		"""
		# check for new model
		if not model:
			model = self. model
  
		# get response from gpt
		response = self._send_gpt_request(speech, model, manual_request, max_tokens)
		# cleanup response
		response = self._clean_response(response, self.bot_name)
	
		return response

	def _send_gpt_request(self, speech:str, model:str, manual_request:bool, max_tokens:int) -> str:
		"""
		Sends a POST request to the GPT model and returns the response.
		"""
		if manual_request:
			message = [{"role": "user", "content": speech}] 
		else:
			self._update_conversation("user", speech)
			message = self.conversation_history
   
		response = openai.ChatCompletion.create(
			model=model,
			messages = message,
   			max_tokens = max_tokens
      		)

		# Extract the 'content' value from the response
		# This is the response from the GPT model
		response = response['choices'][0]['message']['content']
		response = response.strip()
  
		# reset conversation history, for now...
		self.conversation_history = [{"role": "assistant", "content": "You are an assistant capable of answering questions in a friendly and concise manner"}]
  
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
			
