from src.juno import Juno

def main():

	new_bot = Juno()

	# The bot will continuously listen for user input, process it, and produce a response
	# Exit the program by saying a generic exit command such as: 'exit', 'quit', 'terminate', or 'end conversation'
	while True:
		speech = new_bot.listen()
		response = new_bot.process(speech)
		new_bot.verbalize(response)
  
		# or
		# new_bot.run()
         
if __name__ == '__main__':
	main()