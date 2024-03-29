import unittest
from configuration.secrets import key_vault
from src.customization.packages.virtual_assistant.commands.get_weather.get_weather import GetWeather

class TestGetWeather(unittest.TestCase):
    """Class for testing the GetWeather command"""
    
    def setUp(self):
        self.weather_key = key_vault.retrieve_secret('Weather-API')
        
        self.get_weather = GetWeather(self.weather_key)
        self.get_weather_incorrect = GetWeather('wrong_key')
        self.test_location = "Chicago"
        
    def test_get_weather(self):
        response = self.get_weather.get_weather(self.test_location)
        self.assertNotEqual(response, f"Sorry, there was error while retrieving the weather for {self.test_location}. Please try asking again.")

    def test_get_weather_with_incorrect_key(self):
        # Use a wrong key to provoke an error
        response = self.get_weather_incorrect.get_weather(self.test_location)
        self.assertEqual(response, f"Sorry, there was error while retrieving the weather for {self.test_location}. Please try asking again.")
        
if __name__ == '__main__':
    unittest.main()