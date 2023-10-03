from src.juno import Juno

def create_virtual_assistant():
	"""
	.listen() used for user input via microphone  
    .process() used to process and produce a response (Queries GPT with a prompt and recieves the response. 
                                                       Can also detect intent used for custom commands)                                                     
    .verbalize() performs text-to-speech using Azure or ElevenLabs voice engines
    """

	# Create an instance of Juno using the virtual assistant package and a prebuilt profile
	# for creating personalized profiles look in usage\create_profile
	new_assistant = Juno(profile='jessica', package='virtual_assistant')

	# The bot will continuously listen for user input, process it, and produce a response
	# Exit the program by saying a generic exit command such as: 'exit', 'quit', 'terminate', or 'end conversation'
	new_assistant.run()
         
if __name__ == '__main__':
	create_virtual_assistant()