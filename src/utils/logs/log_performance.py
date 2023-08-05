import os
import json
import datetime
import time

# path to 'logs.json'
log_path = os.path.join('src/components/logs', 'log.json')

class PerformanceLogger:
	"""
	A class that logs the performance of a function and stores the data in 'logs.json'
	"""
	
	def __init__(self):
		# today's date
		self.today = datetime.datetime.now().strftime("%Y-%m-%d")
		#self.data = self._load_in_data()
		self.action = None
		self.actions = {'listen': 'Speech Recognition', 'process': 'Speech Processing', 'verbalize_speech': 'Speech Verbalization'}
	
	def _load_in_data(self):
		"""
  		load in data from 'logs.json'
		"""
		try:
			with open(log_path, "r") as f:
				return json.load(f)
		except FileNotFoundError:
			print('The file: "logs.json" was not found')
   
	def _save_data(self, new_log_session):
		"""
  		save data to 'logs.json'
		"""	
		# add new log session to data
		self.data["log_sessions"].append(new_log_session)
  
		with open(log_path, "w") as f:
			json.dump(self.data, f, indent=4)
  
	def _load_fresh_log_template(self):
		return {
                'Session': { 
              				self.action: {
									"Date": self.today,
									"Action Performed": None,
									"Input": None,
									"Output": None,
									"Success": False,
									"Error": None,
									"Run time": None
									} 
                        } 
				}
   
	def	log_operation(self, func):
		"""
		decorator that logs the performance of a function and stores the data in 'logs.json'
		"""
		def wrapper(*args, **kwargs):
   
			# Ex. If func.__name__ == 'listen', actino is 'speech recognition'
			self.action = self.actions[func.__name__]
   
			log_template = self._load_fresh_log_template()

			# Speech recognition is the first action performed in a session
			if self.action == 'Speech Recognition':
				input = f"User input"
			else:
				input = f"{args} {kwargs}"
   
			# record input
			log_template["Session"][self.action]["Input"] = input
   
			# record start time
			start_time = time.perf_counter()

			# record output
			result = func(*args, **kwargs)

			# record end time
			end_time = time.perf_counter()
   
			# record run time
			log_template["Session"][self.action]["Run time"] = end_time - start_time
   
			if result:
				log_template["Session"][self.action]["Success"] = True
				log_template["Session"][self.action]["Output"] = result
			else:
				log_template["Session"][self.action]["Successful"] = False
				log_template["Session"][self.action]["Output"] = 'error'
				log_template["Session"][self.action]["Error"] = result
    
			# save data
			self._save_data(log_template)
	
			return result
		return wrapper
	
