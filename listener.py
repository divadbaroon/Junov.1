from flask import Flask, request
from src.juno import Juno
import threading

app = Flask(__name__)

def start_juno():
    new_bot = Juno()
    # Replace the while loop with new_bot.run() if applicable
    while True:
        speech = new_bot.listen()
        response = new_bot.process(speech)
        new_bot.verbalize(response)

@app.route('/start_juno', methods=['POST'])
def handle_request():
    threading.Thread(target=start_juno).start()
    return "Juno started", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
