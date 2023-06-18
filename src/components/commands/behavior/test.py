from src.components.commands.behavior.behavior import BotBehavior
from settings.settings_orchestrator import SettingsOrchestrator

class TestBotBehavior:
    
    def __init__(self):
        self.bot_settings = SettingsOrchestrator()
        self.bot_behavior = BotBehavior()
        
    def _test_mute(self):
        response = self.bot_behavior.mute()
        