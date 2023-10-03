import yaml
import datetime
import time
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager

class PerformanceLogger:
	"""
	A class that logs the performance of a function and stores the data in 'logs.yaml'
	"""

	def __init__(self):
		self.profile_name = MasterSettingsManager().retrieve_property('profile')
		self.log_path = f'src/profiles/profile_storage/{self.profile_name}/logs.yaml'
		#self._initialize_new_session()
		self.todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
		
	def log_operation(self, func):
		"""
		decorator that logs the performance of a function and stores the data in 'logs.yaml'
		"""
		def wrapper(*args, **kwargs):
			action = func.__name__
			
			if action == 'listen':
				input_data = "User input"
			elif action in ['process_speech', 'verbalize_speech']:
				input_data = args[1]
			elif action == '_retrieve_top_intent':
				input_data = args
				if input_data is None:
					input_data = "ask_gpt"
			else:
				input_data = f"{args} {kwargs}"

			log_template = self._load_fresh_log_template(action)

			log_template[action]["Input"] = input_data

			start_time = time.perf_counter()
			result = func(*args, **kwargs)
			end_time = time.perf_counter()

			log_template[action]["Run time"] = end_time - start_time

			if result: 
				log_template[action]["Success"] = True
				log_template[action]["Output"] = result
			else:
				log_template[action]["Success"] = False
				log_template[action]["Output"] = 'error'
				log_template[action]["Error"] = result

			self._save_data(log_template, action)
			return result
		return wrapper

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

	def _save_data(self, log_entry, action):
		data = self._load_in_data()
		current_time = datetime.datetime.now().strftime("%H:%M:%S")
		
		if self.todays_date not in data:
			data[self.todays_date] = {
				"Time": current_time,
				"Logs": []
			}
		else:
			data[self.todays_date]['Time'] = current_time  # Update time for every log
		
		log_entry_data = {
			"Action": action,
			**log_entry[action]  # This will unpack the inner dictionary
		}
		data[self.todays_date]['Logs'].append(log_entry_data)

		with open(self.log_path, "w") as f:
			yaml.safe_dump(data, f)

	def _load_in_data(self):
		try:
			with open(self.log_path, "r") as f:
				loaded_data = yaml.safe_load(f)
				if loaded_data is None:  # If the file is empty, it will return None
					return {"log_sessions": []}
				return loaded_data
		except (FileNotFoundError, yaml.YAMLError):
			print('The file: "logs.yaml" was not found or is improperly formatted.')
			return {"log_sessions": []}
