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
		
	def get_weather(self, location:str):
		"""
		Fetches the current temperature for a specific location.
		:param location: The name of the location(city name) to get the weather for.
  
		:return: A string containing a human-readable description of the current temperature at the given location.
		"""
		# Clean the user's location input
		location = self._clean_location(location)
		# Get the current temperature for the given location
		location_temperature = self._send_request(location)
		# Return an appropriate response given the location, temperature, and the user's preferred units
		return self._create_response(location, location_temperature)

	def _clean_location(self, location:str) -> str:
		"""
		Cleans the location input to remove any trailing punctuation.
		:param location: The raw location string provided by the user.
  
		:return: The cleaned location string, with any trailing question marks removed.
		"""
		if location.endswith('?'):
			location = location.rstrip('?')
   
		return location

	def _send_request(self, location:str) -> str:
		"""
  		Sends a request to the OpenWeatherMap API for the current temperature of a given location
		:param location: The name of the location to get the weather for. It should be a cleaned string representing a city,
                     state, or country.
                     
    	:return: The current temperature at the given location, in the units specified by `self.units`. If the API request
             fails for any reason, returns None.
  		"""
		try:
			response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&units={self.units}&appid={self.weather_key}")
		except Exception as e:
			print(f"An error occurred while trying to send a request to openweathermap. Error: {e}")
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
		:param location: The name of the location for which weather was requested. 
		:param temperature: The current temperature at the given location, or None if the temperature could not be retrieved.
  
		:return: A string response indicating the current temperature at the given location in the appropriate units. If the
				temperature could not be retrieved, returns an error message instead.
    	"""
		if temperature is None:
			response = f"Sorry, there was error while retrieving the weather for {location}. Please try asking again."
		elif self.units == "imperial":
			response = f"The weather in {location} is {round(temperature)} degrees Fahrenheit"
		else:
			response = f"The weather in {location} is {round(temperature)} degrees Celsius"	
		return response
