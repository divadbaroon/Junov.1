# Azure-Powered-Virtual-Assistant 

## Introduction
This project is a virtual assistant named PiBot that utilizes Azure's Cognitive Services for its speech recognition, speech verbalization, translation, and intent recognition. The bot can be personalized to respond in a specified persona (such as Barack Obama), gender, and language.
The bot currently has the the capability to perform various functions such as speech translation, weather retireval, Google and Youtube searching, muting and unmuting, and ending the program. The user's intent for command execution is detected using Azure's LUIS service. If substantial intent for a command is found, then the intended action takes place. If minimal intent is detected a response is created using Open AI's chatGPT. The bot's conversation history is kept in the file "conversation_history.json" and cleared at the end of the program. 

## Requirements
- Azure account and subscription
- The following Azure Resources:
  - A LUIS resource with an accompanying prediction resource
  - A Speech Service resource
  - A Translator resource
- An Azure Key Vault to store the following secrets
  - Azure LUIS API key
  - Azure LUIS APP ID
  - OpenAI API key
  - Azure Speech Service API key
  - OpenWeatherMap API key
- Python 3.x

## Installation
1. Clone the repository: `git clone https://github.com/divadbaroon/Azure-Powered-Virtual-Assistant.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Create all necessary resources that were stated in the requirements within your Azure account
4. Obtain and secure all keys stated above in an Azure Key Vault
5. Copy the contents of sample_config.py to a new file called config.py.
6. Replace the placeholder values in config.py with your own Azure Key Vault name and secrets.
7. Ensure all the calls to sample_config throughout the script match the names you gave to the secrets in your Key Vault

## Usage
1. Open your terminal or command prompt
2. Change into your folder's directory
3. Run the program: python main.py
4. Choose whether to customize your bot
5. Wait for "listening..." to appear, indicating that the bot is now listening for input
6. Interact with the bot by speaking

## How to interact with the bot
- Note: The command recognition is done using your trained LUIS model, thus the way you give your commands should be able to vary greatly

| Command | Response |
| ------- | -------- |
| What is the weather in {location} | {location}'s {temperature} in fahrenheit |
| Translate {speech} into {language} | A verbal {translation} of speech into {language}|
| Open {website} | {website} is opened |
| Search {speech} | Conducts a google search with {speech} |
| Search youtube for {speech} | Conducts a youtube search for {speech} |
| Mute | Bot is now muted |
| Unmute | Bot is now unmuted |
| Exit | Ends the program |

## Help
 - How to make an Azure account and subscription.
   - https://learn.microsoft.com/en-us/training/modules/create-an-azure-account/
 - How to create a LUIS, Speech Service, and Translator resource.
   - The resources are located under the "Create a new Azure Cognitive Services resource" subheading 
   - https://learn.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=language%2Canomaly-detector%2Clanguage-service%2Ccomputer-vision%2Cwindows 
 - How to create an Azure Key Vault
   - https://learn.microsoft.com/en-us/azure/key-vault/general/quick-create-portal
 - How to train a LUIS model
   - https://learn.microsoft.com/en-us/azure/cognitive-services/luis/how-to/train-test
  
 
