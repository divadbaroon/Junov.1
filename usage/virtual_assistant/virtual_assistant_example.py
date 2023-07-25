from src.juno import Juno

def main():
	# Create an instance of Juno using the virtual assistant package
	new_bot = Juno(package='virtual_assistant')

	# The bot will continuously listen for user input, process it, and produce a response
	# Exit the program by saying a generic exit command such as: 'exit', 'quit', 'terminate', or 'end conversation'
	new_bot.run()
         
if __name__ == '__main__':
	main()