import time

class StartTimer:
	"""A class to start a timer for a given amount of time."""
	
	def __init__(self, speech_verbalizer):
		self.speech_verbalizer = speech_verbalizer
		
	def start_timer(self, user_time, metric):
		self.speech_verbalizer.verbalize_speech(f'Ok, I will start a timer for {user_time} {metric[0]}')
		user_time = self._convert_to_seconds(user_time, metric)
		
		# start timer
		time.sleep(int(user_time))
  
		return 'Time is up!'
		
	def _convert_to_seconds(self, user_time, metric):
		"""Starts a timer for a given amount of time."""
		# Convert user_time to seconds
		if metric == 'seconds' or metric == 'second':
			pass
		elif metric == 'minutes' or metric == 'minute':
			user_time *= 60
		elif metric == 'hours' or metric == 'hour':
			user_time *= 3600
   
		return user_time

	
	
	

