from src.juno import Juno

def create_virtual_assistant():
	"""
	Agents are created using Juno and use the following methods to interact:
 
	.listen() used for user input via microphone  
    .process() used to process and produce a response (Queries GPT with a prompt and recieves the response. 
                                                       Can also detect intent used for custom commands)                                                     
    .verbalize() performs text-to-speech using Azure or ElevenLabs voice engines
    """

	# Create an instance of Juno using the virtual assistant package and a prebuilt profile
	# for creating personalized profiles look in usage\create_new_profile.py
	new_bot = Juno(profile='jessica', package='virtual_assistant')

	# The bot will continuously listen for user input, process it, and produce a response
	# Exit the program by saying a generic exit command such as: 'exit', 'quit', 'terminate', or 'end conversation'
	new_bot.run()
         
if __name__ == '__main__':
	create_virtual_assistant()