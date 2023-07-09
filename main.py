from src.pibot import PiBot

def main():
	# Create an instance of pibot
	new_bot = PiBot(role='virtual assistant', gender='female', language='english')

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