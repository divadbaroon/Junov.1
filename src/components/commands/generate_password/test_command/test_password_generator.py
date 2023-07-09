import unittest
from src.components.commands.password_generator.password_generator import PasswordGenerator

class TestPasswordGenerator(unittest.TestCase):
    """Class for testing the PasswordGenerator command"""
    
    def setUp(self):
        self.password_generator = PasswordGenerator()
        
    def test_password_generator(self):
        response = self.password_generator.generate_password(copy_to_clipboard=False)
        self.assertEqual(response, f'A random password has been created.')
        
if __name__ == '__main__':
    unittest.main()