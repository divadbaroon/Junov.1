import requests

class GetWeather:
	"""
	A class that gets the weather for a given location.
	"""
		
	def get_weather(self, location:str, weather_key:str):
		"""
		Gets the weather for a given location.
		:param location: (str) the location to get the weather for
		:return: (str) the weather for the given location
		"""
				
		# The location sometimes ends in a question mark
		if location.endswith('?'):
			location = location.rstrip('?')
			
		# Attempt to send request to openweathermap api
		try:
			response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_key}")
		except Exception as e:
			print(f"An error occurred while trying to send a request to openweathermap. Error: {e}")
			response = "Sorry, an error has occured. Please try asking again."
			return response

		# Check whether request was successful
		if response.status_code == 200:
		
			# Returned json file with weather data
			data = response.json()

			temperature = data["main"]["temp"]

			# Convert temperature from kelvin to fahrenheit
			temperature_fahrenheit = (temperature - 273.15) * 9/5 + 32

			response = f"The weather in {location} is {round(temperature_fahrenheit)} degrees Fahrenheit"		
		else:
		
			print(f"An error occurred while trying to send a request to openweathermap. Error: {response.status_code}")
			response = "Sorry, an error has occured. Please try asking again."
				
		return response
