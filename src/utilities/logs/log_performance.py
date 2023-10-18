import yaml
import time 
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager
from src.customization.profiles.profile_manager import ProfileManager

class PerformanceLogger:
	"""
	Logs the performance of each method in a session
	"""
 
	def __init__(self):
		self.profile_name = MasterSettingsManager().retrieve_property('profile')
		self.entity_name = ProfileManager().retrieve_property('name', self.profile_name)
		self.log_path = f'src/customization/profiles/profile_storage/{self.profile_name}/logs.yaml'
		self.new_session = True
  
	def log_operation(self, func):
		"""
		Decorator that logs the performance of each method in a session
		"""
		def wrapper(*args, **kwargs):
			"""
			Wrapper function that logs the performance of each method in a session
			"""
   
			# get name of function
			action = func.__name__
   
			# Determine input_data based on the action (function name)
			action = self._make_method_name_readable(action, args, kwargs)

			# Log the operation
			result = self._log_operation(action, func, *args, **kwargs)
			return result
		return wrapper
   
	def _make_method_name_readable(self, action: str, args, kwargs) -> str:
		"""
		Converts a method name to a human-readable string
		"""
		# Determine input_data based on the action (function name)
		if action == 'listen':
			action = "User input"
		elif action in ['process_speech', 'verbalize_speech']:
			action = args[1]
		elif action == '_retrieve_top_intent':
			action = args
			if action is None:
				action = "ask_gpt"
		else:
			action = f"{args} {kwargs}"
   
	def _log_operation(self, action: str, func, *args, **kwargs):
		"""
		Logs the operation
		"""
		# Load the log template
		log_data = self._load_fresh_log_template(action)
  
		# Time the operation
		start_time = time.perf_counter()
		# Get the result of the function
		result = func(*args, **kwargs)
		end_time = time.perf_counter()

		# Save runtime
		log_data[action]["Run time"] = end_time - start_time

		# Save input_data
		if result: 
			log_data[action]["Success"] = True
			log_data[action]["Output"] = result
		else:
			log_data[action]["Success"] = False
			log_data[action]["Output"] = 'error'
			log_data[action]["Error"] = result

		self._save_data(log_data)
  
		return result
   
	def _load_fresh_log_template(self, action):
		return {
			action: {
				"Input": None,
				"Output": None,
				"Success": False,
				"Errors": None,
				"Run time": None
			}
		}
  
	def _save_data(self, log_data):
		"""
		Saves the log operation
		"""
		existing_data = self._Load_in_data()
		log_data.update(existing_data)
		try:
			with open(self.log_path, "w", encoding="utf-8") as f:
				yaml.safe_dump(log_data, f)
		except FileNotFoundError:
			print('The file "logs.yaml" is missing. Make sure all files are located within the same folder.')
		 
	def _Load_in_data(self):
		"""
		Loads the log data
		"""
		try:
			with open(self.log_path, 'r', encoding='utf-8') as f:
				data = yaml.safe_load(f) or {}
		except FileNotFoundError:
			print('The file "logs.yaml" is missing.\nMake sure all files are located within the same folder.')
			data = {}
		return data