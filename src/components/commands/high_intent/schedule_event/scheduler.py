from datetime import date, datetime, timedelta
import sched
import time
import threading

class Scheduler:
	"""Sets an alarm for a given time"""
	
	def __init__(self, command_settings:object):
		self.command_settings = command_settings
		self.scheduler = sched.scheduler(time.time, time.sleep)
		self.alarm_time = None
		self.response = None
		today = date.today()
		self.day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		self.day_of_week = self.day_names[today.weekday()]
  
	def set_reminder(self, hour, minute, second, am_or_pm, reminder):
		# attempt to format user given time as "Hour:Minute:Second"
		try:    
			self._format_time(hour, minute, second, am_or_pm)
		except ValueError:
			return 'Beep beep boop boop, error setting a reminder. Please try asking again.'

		self._schedule_event(reminder)
  
		self.command_settings.save_property(command="set_reminder", setting='end_time', value=f"{self.day_of_week}, {self.alarm_time}")
		self.command_settings.save_property(command="set_reminder", setting='time', value=f"{self.day_of_week}, {self.alarm_time}")
  
		self.response = f'I have set an reminder for {self.day_of_week} at {self.alarm_time} {am_or_pm}'
		return self.response
		
	def set_alarm(self, hour, minute, second, am_or_pm:str):
     
		# attempt to format user given time as "Hour:Minute:Second"
		try:    
			self._format_time(hour, minute, second, am_or_pm)
		except ValueError as e:
			return 'Beep beep boop boop, error setting alarm. Please try asking again.'

		self._schedule_event()

		self.command_settings.save_property(command="set_alarm", setting='end_time', value=f"{self.day_of_week}, {self.alarm_time}")
  
		self.response = f'I have set an alarm for {self.day_of_week} at {self.alarm_time} {am_or_pm}'
		return self.response

	def _schedule_event(self, reminder=None):

		time_struct = time.strptime(self.alarm_time, "%H:%M:%S")

		self.alarm_time = time.strftime("%H:%M:%S", time_struct)

		# Adjust the date to tomorrow if the time is in the past
		now = datetime.now()
		alarm_datetime = datetime.combine(now.date(), datetime.strptime(self.alarm_time, "%H:%M:%S").time())
		if alarm_datetime < now:
			alarm_datetime = alarm_datetime + timedelta(days=1)

		# Convert the datetime object into a timestamp
		event_time = time.mktime(alarm_datetime.timetuple())

		# Define the action to be taken when the event triggers
		event_action = lambda: self.trigger_event(reminder)

		# Schedule the event
		self.scheduler.enterabs(event_time, 1, event_action, ())
		
		# Start the scheduler in a separate thread
		thread = threading.Thread(target=self.scheduler.run)
		thread.start()
	
	def trigger_event(self, reminder):
		if reminder:
			print(f'Here is your reminder: {reminder}')
			# reset settings
			self.command_settings.save_property(command="set_reminder", setting='end_time', value="")
			self.command_settings.save_property(command="set_reminder", setting='time', value="")
			return f'Here is your reminder: {reminder}'
		else:
			print('Alarm has triggered!')
			# reset setting
			self.command_settings.save_property(command="set_alarm", setting='end_time', value="")
			return 'Alarm has triggered!'
		
	def cancel_event(self):
		# Cancel the scheduled alarm
		self.scheduler.cancel(self.scheduler.queue[0])  
		return 'Alarm has been canceled'
  
	def _format_time(self, hour, minute, second, time_of_day:str):
		# convert to 24 hour format: "%H:%M:%S"
		if time_of_day.lower() in ['pm', 'evening', 'night']:
			if hour != 12:  
				hour += 12  
			self.alarm_time = f"{hour}:{minute}:{second}"
		elif time_of_day.lower() in ['am', 'morning']:
			if hour == 12:  
				hour = 0  
			self.alarm_time = f"{hour:02d}:{minute:02d}:{second:02d}"
		else:
			self.response = "Please specify either 'AM' or 'PM'."
   
# Example usage
# test = Scheduler()
# print(test.set_reminder(hour=11, minute=35, second=0, am_or_pm="am", reminder='hi'))  
