# Azure-Powered Virtual Assistant Chatbot

## Introduction
This project is a virtual assistant chatbot that utilizes Azure's Cognitive Services for its speech recognition and speech verbalization. 
The bot currently has the the capability to translate speech, get weather information for a specified location, search google, open a website,
search youtube, mute and unmute itself, and exit the program. The user's intent is detected using Azure's LUIS service and an appropriate action or response is produced. 
If minimal intent is detected a response is created using Open AI's chatGPT.

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
3. Create all necessary resources that were stated in the requirements within Azure
4. Obtain and secure all keys stated above in an Azure Key Vault
5. Replace the placeholder in `sample_config.py` with your own Azure Key Vault name
6. Ensure all calls to the sample_config throughout the script match the names you gave the secrets in your Key Vault

## Usage
The chatbot listens for user input and responds appropriately. The user can interact with the chatbot by speaking or typing.
