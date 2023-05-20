# Azure-Powered-Virtual-Assistant 
## Project Overview
PiBot is an open-source virtual assistant that leverages Azure's Cognitive Services for speech recognition, text-to-speech, translation, and intent recognition. It aims to provide a customizable alternative to mainstream virtual assistants like Alexa.

### User Intent and Interaction
The system uses a trained Azure CLU model to detect user intent. If the user's intent for a prebuilt command is minimal, PiBot intelligently generates responses using OpenAI's GPT-3 API to ensure meaningful interactions.

### Conversation History and Context Awareness
To maintain context awareness and avoid repetition, PiBot keeps a conversation history in the "conversation_history.json" file. After each program session, this history is cleared.

### Utilizing GPT-3
However, the conversation history is fed back into GPT-3 for each response, as GPT-3's current API model does not inherently utilize past conversation history. This approach allows PiBot to provide context
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
7. Ensure all the calls to config throughout the script match the names you gave to the secrets in your Key Vault

## Usage
1. Open your terminal or command prompt
2. Change into your folder's directory
3. Run the program: python main.py
4. Choose whether to customize your bot
5. Wait for the startup sound to play, indicating that the bot is now listening for input
6. Interact with the bot by speaking

## Training Your Model
This section provides instructions on how to train your own Conversational Language Understanding (CLU) model using Azure. The model is used to understand and interpret the user's intent during the conversation. The training data is provided in the "PiBot_Training_Data.json" file located within the "training_data" folder.
1. **Sign in to Azure:** Access the Azure portal and sign in using your Azure account. If you don't have an account, you'll need to create one.
2. **Access the CLU Dashboard:** Navigate to the Conversational Language Understanding Dashboard using the following link: https://language.cognitive.azure.com/clu/projects.
3. **Import the training data:** On the dashboard, look for an "Import" button. Click this button and a dialog box will appear prompting you to upload a file.
4. **Upload the training data file:** Locate the "PiBot_Training_Data.json" file within the "training_data" folder of your project directory. Select this file and click "Open" or "Upload" in the dialog box.
5. **Begin a training session:** After the upload is complete, navigate to the "Training Jobs" section on the dashboard. Here, you'll see an option to start a new training session. Click on it to commence the training process using the data you've just uploaded.
6. **Deploy your trained model:** After the training session is complete, your model needs to be deployed to be used by the program. To do this, navigate to the "Deploying a model" section on the dashboard. Follow the instructions to deploy your newly trained model.

By following these steps, you're training your virtual assistant on a large dataset of potential conversational commands, improving its ability to understand and respond to user commands effectively.

## Supported Commands
The command recognition is done using your trained CLU model, allowing for versatile command phrasing.

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
| Change persona to {persona} | Changes the persona of the bot to {persona} |
| Change gender to {gender} | Changes the gender of the bot to {gender} |
| Change language to {language} | Changes the language of the bot to {language} |
| Get conversation history | Retrieves conversation history |
| Mute | Mutes the bot's responses |
| Unmute | Unmutes the bot's responses |
| Pause | Pauses all of the bot's functionalities |
| Exit | Terminates the program |

Note: If a command is given that is not included in the above list, a response will be given using GPT.

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
