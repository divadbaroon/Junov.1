import unittest

# import all command test classes
from src.components.commands.low_intent.ask_gpt.test_command.test_ask_gpt import TestAskGPT
from src.components.commands.high_intent.bot_behavior.test_command.test_bot_behavior import TestBotBehavior
from src.components.commands.high_intent.get_weather.test_command.test_get_weather import TestGetWeather
from src.components.commands.high_intent.set_timer.test_command.test_timer import TestStartTimer
from src.components.commands.high_intent.translate_speech.test_command.test_translate_speech import TestTranslateSpeech
from src.components.commands.high_intent.web_searcher.test_command.test_web_searcher import TestWebSearcher

def comprehensive_test():
    """
    Performs a comprehensive test on all bot functionalites and commands
    """
    
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    suite.addTests(loader.loadTestsFromTestCase(TestAskGPT))
    suite.addTests(loader.loadTestsFromTestCase(TestBotBehavior))
    suite.addTests(loader.loadTestsFromTestCase(TestGetWeather))
    suite.addTests(loader.loadTestsFromTestCase(TestStartTimer))
    suite.addTests(loader.loadTestsFromTestCase(TestTranslateSpeech))
    suite.addTests(loader.loadTestsFromTestCase(TestWebSearcher))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(comprehensive_test())

