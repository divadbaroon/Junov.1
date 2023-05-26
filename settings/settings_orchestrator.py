from settings.conversation_history.conversation_history_manager import ConversationHistoryManager
from settings.bot_settings.bot_settings_manager import BotSettingsManager
from settings.voice_settings.voice_settings_manager import VoiceSettingsManager

class SettingsOrchestrator:
    """Orchestrates the settings managers for the following files:
    "conversation_history.json", "bot_settings.json", and "voice_settings.json"""
    def __init__(self):
        self.conversation_manager = ConversationHistoryManager()
        self.bot_settings = BotSettingsManager()
        self.voice_settings = VoiceSettingsManager()

    def retrieve_bot_property(self, property: str) -> str:
        """Retrieves a property from "bot_settings.json" and returns it."""
        return self.bot_settings.retrieve_property(property)
    
    def save_bot_property(self, setting: str, value: str) -> str:
        """Save a property to "bot_settings.json."""
        self.bot_settings.save_property(setting, value)
        
    def reload_bot_settings(self) -> None:
        """Reloads the data in "bot_settings.json"."""
        self.bot_settings.reload_settings()
    
    def retrieve_voice_name(self, gender: str, language: str) -> str:
        """Retrieves a voice name pertaining to a specific gender and language from "voice_settings.json" and returns it."""
        return self.voice_settings.retrieve_voice(gender, language)
    
    def retrieve_voice_names(self, gender: str, language:str) -> list:
        """Retrieves all voice names pertaining to a specific gender from "voice_settings.json" and returns them as a list."""
        return self.voice_settings.retrieve_voices(gender, language)
    
    def retrieve_available_languages(self) -> list:
        """Retrieves all voice names pertaining to a specific gender from "voice_settings.json" as a list."""
        return self.voice_settings.available_languages()
    
    def retrieve_language_code(self, language: str) -> str:
        """
        Retrieves the language code associated with a specified language
        from "voice_settings.json"
        """
        return self.voice_settings.retrieve_language_code(language)
    
    def get_language_country_code(self, language:str) -> str:
        """Gets the country code for the given language"""
        return self.voice_settings.retrieve_language_country_code(language)

    def load_conversation_history(self) -> list:
        """
		Loads the conversation history from the conversation_history.json file
		"""
        return self.conversation_manager.load_conversation_history()
    
    def get_conversation_history(self, persona: str) -> str:
        """
		Gets the conversation history from the conversation_history.json file
		and prints it to the console
		"""
        return self.conversation_manager.get_conversation_history(persona)
    
    def save_conversation_history(self, speech: str, response: str, persona: str) -> None:
        """
		Saves the new conversation along with the rest of the conversation
		history to conversation_history.json file
		"""
        self.conversation_manager.save_conversation_history(speech, response, persona)
        
    def clear_conversation_history(self) -> str:
        """
		Clears the conversation history
		"""
        return self.conversation_manager.clear_conversation_history()

    def exit_and_clear_conversation_history(self) -> str:
        """
		Clears the conversation history and exits the program
		"""
        return self.conversation_manager.exit_and_clear()


    

