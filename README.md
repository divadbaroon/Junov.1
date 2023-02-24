# Azure-Powered-Virtual-Assistant 

## Introduction
This project is a virtual assistant named PiBot that utilizes Azure's Cognitive Services for its speech recognition, speech verbalization, translation, and intent recognition. The bot can be personalized to respond in a specified persona, such as Barack Obama, Tony Stark, Jimmy Kimmel, etc., gender, and language (see supported langauges below).

PiBot has the the capability to perform various functions such as speech translation, weather retireval, Google and Youtube searching, muting and unmuting, and ending the program on command. The user's intent for command execution is detected using a trained Azure LUIS model. If substantial intent for a command is found, then the intended action takes place. If minimal intent is detected a response is created using Open AI's chatGPT. 

The bot's conversation history is kept in the file "conversation_history.json" and cleared at the end of the program. Since ChatpGPT's current API model is not capable of using past conversation history, the conversation history is fed back into chatGPT for each response. This is to help the bot have context for its responses and avoid repeating itself.

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

## Supported Commands
The command recognition is done using your trained LUIS model, allowing for versatile command phrasing.

### Weather
| Command | Response |
| ------- | -------- |
| What is the weather in {location} | Provides the current temperature in {location} |
### Translation
| Command | Response |
| ------- | -------- |
| Translate {speech} into {language} | Translates {speech} into {language} |
### Web Browsing
| Command | Response |
| ------- | -------- |
| Open {website} | Opens the specified {website} |
| Search {speech} | Conducts a Google search for {speech} |
| Search youtube for {speech} | Conducts a YouTube search for {speech} |
### Bot Functionalities
| Command | Response |
| ------- | -------- |
| Generate a random password | Generates a random password and copies it to the users clipboard |
| Get conversation history | Retrieves conversation history |
| Mute | Mutes the bot's responses |
| Unmute | Unmutes the bot's responses |
| Pause | Pauses all of the bot's functionalities |
| Exit | Terminates the program |

Note: If a command is given that is not included in the above list, a response will be given using chatGPT.

### Sample Conversation History
- Note: Conversation history is stored in the file "conversation_history.json"
- For this conversation the bot was setup with the following characteristics: 
  - Persona = Barack Obama 
  - Gender = Male 
  - Language = English_USA
```
{
    "conversation": [
        {
            "User": "hello, who are you?",
            "Barack Obama": "Hello there! My name is Barack Obama. It's nice to meet you."
        },
        {
            "User": "what was it like to be president?",
            "Barack Obama": "It was an incredible honor and a great responsibility to serve as President of the United States. It was a privilege to work on behalf of the American people and to help shape our country's future."
        },
        {
            "User": "what was the greatest challenge you faced as president?",
            "Barack Obama": "The greatest challenge I faced as President was the economic crisis that began in 2008. It was a difficult time for the country and for the world, but I was determined to make sure that we responded in a way that was fair and responsible. We were able to put in place policies that helped stabilize the economy, create jobs, and get our country back on the right track."
        },
        {
            "User": "what's your favorite vacation spot?",
            "Barack Obama": "My favorite vacation spot is Hawaii. I love the sunshine, the beautiful beaches, and the warm hospitality of the people. It's a great place to relax and unwind."
        },
        {
            "User": "what is the weather in chicago?",
            "Barack Obama": "The weather in chicago is 34 degrees Fahrenheit"
        },
        {
            "User": "open google",
            "Barack Obama": "Opening google.com" 
            # This action opens Google.com in the user's web browser
        },
        {
            "User": "search youtube for videos of obama dancing",
            "Barack Obama": "Searching youtube for videos of obama dancing" 
            # This action performs a Youtube search for "videos of obama dancing" and opens it in the user's web browser
        },
        {
            "User": "translate hey, how's it going into french?",
            "Barack Obama": "Hé, comment ça va"
        }
    ]
}
``` 
## Help
 - How to make an Azure account and subscription.
   - https://learn.microsoft.com/en-us/training/modules/create-an-azure-account/
 - How to create a LUIS, Speech Service, and Translator resource.
   - The resources are located under the "Create a new Azure Cognitive Services resource" subheading 
   - https://learn.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=language%2Canomaly-detector%2Clanguage-service%2Ccomputer-vision%2Cwindows 
 - How to create an Azure Key Vault.
   - https://learn.microsoft.com/en-us/azure/key-vault/general/quick-create-portal
 - How to create and train an Azure LUIS model.
   - https://learn.microsoft.com/en-us/azure/cognitive-services/luis/how-to/sign-in
   
 ## Supported Langauges
 Arabic, English (Australia, Ireland, UK, USA), Finnish, French, German, Hindi, Korean, Mandarin, Russian, Spanish
