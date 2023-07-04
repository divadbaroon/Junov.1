import unittest

# import all command test classes
from ..code.components.commands.ask_gpt.test_command.test_ask_gpt import TestAskGPT
from ..code.components.commands.bot_behavior.test_command.test_bot_behavior import TestBotBehavior
from ..code.components.commands.get_weather.test_command.test_get_weather import TestGetWeather
from ..code.components.commands.password_generator.test_command.test_password_generator import TestPasswordGenerator
from ..code.components.commands.timer.test_command.test_timer import TestStartTimer
from ..code.components.commands.translate_speech.test_command.test_translate_speech import TestTranslateSpeech
from ..code.components.commands.web_searcher.test_command.test_web_searcher import TestWebSearcher

def comprehensive_test():
    """
    Performs a comprehensive test on all bot functionalites and commands
    """
    
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    suite.addTests(loader.loadTestsFromTestCase(TestAskGPT))
    suite.addTests(loader.loadTestsFromTestCase(TestBotBehavior))
    suite.addTests(loader.loadTestsFromTestCase(TestGetWeather))
    suite.addTests(loader.loadTestsFromTestCase(TestPasswordGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestStartTimer))
    suite.addTests(loader.loadTestsFromTestCase(TestTranslateSpeech))
    suite.addTests(loader.loadTestsFromTestCase(TestWebSearcher))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(comprehensive_test())
