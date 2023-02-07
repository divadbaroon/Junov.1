# Azure-Powered Virtual Assistant Chatbot

## Introduction
This project is a virtual assistant named PiBot that utilizes Azure's Cognitive Services for its speech recognition and speech verbalization. 
The bot currently has the the capability to translate speech, get weather information for a specified location, search google, open a website,
search youtube, mute and unmute itself, and exit the program. The user's intent is detected using Azure's LUIS service and an appropriate action or response is produced. If minimal intent is detected a response is created using Open AI's chatGPT.

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

## How to
 - How to make a Azure account and subscription.
   - https://learn.microsoft.com/en-us/training/modules/create-an-azure-account/
 - How to create a LUIS, Speech Service, and Translator resource.
   - The resources are located under the "Create a new Azure Cognitive Services resource" subheading 
   - https://learn.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=language%2Canomaly-detector%2Clanguage-service%2Ccomputer-vision%2Cwindows
  
 
