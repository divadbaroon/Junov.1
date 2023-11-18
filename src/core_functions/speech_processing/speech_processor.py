from .intent_recognition import CLUIntentRecognition
from .command_orchestrator import CommandOrchestrator
from ...utilities.conversation_history.conversation_history_manager import ConversationHistoryManager
from src.utilities.logs.log_performance import PerformanceLogger

import streamlit as st

logger = PerformanceLogger()

class SpeechProcessor:
	"""
	A class that retrieves the user's intent using a trained CLU model and executes an appropriate response and action.
	"""
 
	def __init__(self, api_keys: dict, setting_objects:dict, speech_verbalizer:object):
		self._initialize_settings(setting_objects)
		self.profile_settings = setting_objects['profile_settings']
		self.get_intent = CLUIntentRecognition(api_keys, self.profile_settings, self.voice_settings)
		self.command_orchestrator = CommandOrchestrator(api_keys, speech_verbalizer, None, setting_objects)
		self.manage_conversation_history = ConversationHistoryManager()

	#@logger.log_operation
	def process_speech(self, speech:str) -> str: 
		"""
		Processes the user's input using a trained CLU model (if a package is being used) and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken if applicable
		"""
		print('\nThinking...')
  
		# If a package is provided, retrieve the user's intent using the trained CLU model
		self._check_for_package(speech)

		# Process the user's speech and return the appropriate response and action
		response = self.command_orchestrator.process_command(speech)
  
		# Save conversation history
		if self.save_conversation_history:
			self.manage_conversation_history.save_conversation_history(speech, response)
   
		# Print the response to the user's speech
		print('\nResponse:')
		print(f'{self.bot_name.title()}: {response}')
  
		# If the gui is being used, write the entity response to it
		#if self.gui:
			#self._write_response_to_gui(response)
  
		return response

	def _write_response_to_gui(self, result) -> None: 
		"""
		Write response to gui if it is being used
		"""
		if self.bot_name:
			with st.chat_message("assistant"):
				st.write(f'{self.bot_name.title()}: {result}')
		else:
			with st.chat_message("assistant"):
				st.write(f'Entity: {result}')

	def _check_for_package(self, speech) -> None:
		"""
		Handles the user's speech if a package is provided.
		"""
		if self.package_name: 
			# Returns a dictionary containing similarity rankings between the user's speech and the trained CLU model
			intents_data = self.get_intent.get_user_intent(speech)
			# Updates the intents_data property in the command_orchestrator object with the intents data retrieved from the CLU model
			self.command_orchestrator.intents_data = intents_data
	
	def _initialize_settings(self, setting_objects) -> None:
		"""
		Initialize setting objects.
		"""
		self.master_settings = setting_objects['master_settings']
		self.profile_settings = setting_objects['profile_settings']
		self.voice_settings = setting_objects['voice_settings']
		self.profile = self.master_settings.retrieve_property('profile')
		self.package_name = self.profile_settings.retrieve_property('package')
		self.save_conversation_history = self.master_settings.retrieve_property('functions', 'save_conversation_history')
		self.bot_name = self.profile_settings.retrieve_property('name', self.profile)
		self.gui = self.master_settings.retrieve_property('functions', 'gui')
