import unittest
from unittest.mock import Mock
from src.components.commands.high_intent.set_timer.set_timer import StartTimer  

class TestStartTimer(unittest.TestCase):
    """Class for testing the StartTimer command"""
    
    def setUp(self):
        self.speech_verbalizer = Mock()
        self.start_timer = StartTimer(self.speech_verbalizer)
        
    def test_ask_GPT(self):
        response = self.start_timer.start_timer(.01, "second")
        self.assertEqual(response, "Time is up!")
        
if __name__ == '__main__':
    unittest.main()
