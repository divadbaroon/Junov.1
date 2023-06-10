from src.pibot import PiBot

def main():
	# Create an instance of pibot
	new_bot = PiBot(persona='virtual assistant', gender='female', language='english')

	# The bot will continuously listen for user input, process it, and produce a response
	# Exit the program by saying a generic exit command such as: 'exit', 'quit', 'terminate', or 'end conversation'
	while True:
		# Listen for user input
		speech = new_bot.listen()
		# Process and produce a response/action to user input
		response = new_bot.process(speech)
		# Verbalize the response
		new_bot.verbalize(response)

		# Or run all methods at once
		# new_bot.run()      
		
if __name__ == '__main__':
	main()