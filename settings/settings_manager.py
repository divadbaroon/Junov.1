from settings.conversation.conversation_history_manager import ConversationHistoryManager
from settings.bot_settings.bot_settings_manager import BotSettingsManager
from settings.voice_settings.voice_settings_manager import VoiceSettingsManager

class SettingsOrchestrator:
    def __init__(self):
        self.conversation_manager = ConversationHistoryManager()
        self.bot_settings = BotSettingsManager()
        self.voice_settings = VoiceSettingsManager()

    def get_bot_property(self, property):
        return self.bot_settings.retrieve_property(property)
    
    def get_voice_property(self, property):
        return self.voice_settings.retrieve_property(property)

    def get_conversation_history(self, persona):
        return self.conversation_manager.get_conversation_history(persona)
    
    def save_conversation_history(self, speech, response, persona):
        self.conversation_manager.save_conversation_history(speech, response, persona)
        
    def clear_conversation_history(self):
        return self.conversation_manager.clear_conversation_history()

    def exit_and_clear(self):
        return self.conversation_manager.exit_and_clear()

    def save_bot_property(self, setting, value):
        self.bot_settings.save_property(setting, value)

    def get_language_country_code(self, language):
        return self.voice_settings.get_language_country_code(language)
    
    def reload_settings(self):
        self.bot_settings.reload_settings()

