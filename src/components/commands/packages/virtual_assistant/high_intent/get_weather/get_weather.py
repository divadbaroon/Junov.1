import requests
from src.components.settings.command_settings.command_settings_manager import BotCommandManager

class GetWeather:
	"""
	 A class to interact with the OpenWeatherMap API and provide weather information.
	"""
 
	def __init__(self, weather_key:str):
		self.weather_key = weather_key
		self.command_manager = BotCommandManager()
		self.units = self.command_manager.retrieve_property(command='get_weather', setting='units')
		self.default_location = self.command_manager.retrieve_property(command='get_weather', setting='default_location')
		
	def get_weather(self, location:str) -> str:
		"""
		Fetches the current temperature for a specific location.
		"""
		if location:
			# Clean the user's location input
			location = self._clean_location(location)
		else:
			# use default location if one is not provided
			location = self.default_location 
   
		# Get the current temperature for the given location
		location_temperature = self._send_request(location)
		# Return an appropriate response given the location, temperature, and the user's preferred units
		return self._create_response(location, location_temperature)

	def _clean_location(self, location:str) -> str:
		"""
		Cleans the location input to remove any trailing punctuation.
		"""
		if location.endswith('?'):
			location = location.rstrip('?')
   
		return location

	def _send_request(self, location:str) -> str:
		"""
  		Sends a request to the OpenWeatherMap API for the current temperature of a given location
  		"""
		try:
			response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&units={self.units}&appid={self.weather_key}")
		except Exception as e:
			response = "Sorry, an error has occured. Please try asking again."
			return response

		# Check whether request was successful
		if response.status_code == 200:
		
			# Returned json file with weather data
			data = response.json()

			temperature = data["main"]["temp"]
			return temperature
		else:	
			return None

	def _create_response(self, location:str, temperature:float) -> str:
		"""
  		Creates a user-friendly response based on the retrieved temperature.
    	"""
		if temperature is None:
			response = f"Sorry, there was error while retrieving the weather for {location}. Please try asking again."
		elif self.units == "imperial":
			response = f"The weather in {location} is {round(temperature)} degrees Fahrenheit"
		else:
			response = f"The weather in {location} is {round(temperature)} degrees Celsius"	
		return response
