# Juno 
A platform designed for effortless setup, training, and usage in creating intelligent text-to-speech based agents. Juno was designed to be modular, customizable, and extensible making it suitable for a wide range of use cases.

<details>
<summary><b>Key Features :star:</summary>
   
### Azure Powered 

- Leverages Azure's Cognitive Services for speech recognition, intent recognition, and text-to-speech capabilities. Elevenlabs is also available as an alternate option for text-to-speech.

### Human-Like Interactions 

- Integrates OpenAI's GPT-3.5-Turbo to provide a more natural, human-like conversation experience.

### Broad Conversational Skills 

- Trained on an extensive dataset that covers a wide range of conversational commands, providing efficient responses across diverse scenarios and inquiries.

### Built-In Commands 

- Commands come in packages for specific use cases. See the 'Supported Packages' section for more details.

### Contextual Awareness 

- Stores and utilizes conversation history to provide contextual awareness to the agents.
  
</details>

## Requirements
- Azure account and subscription
- Python 3.x
- Terraform 1.4.6

## Installation Guide

Follow these steps to install and configure the project. Execute all commands from the root directory of the project.

<details>
<summary><b>Steps 🔽 </b></summary>

### Step 1: Install Required Packages

Run the following command to install the necessary packages:

```bash
pip install -r requirements.txt
```

### Step 2: Customize Configuration

Open the secret configuration file in your text editor for customization:

```bash
code configuration/secrets/secret_config.yaml
```
Update the file with your personal settings and save it.

### Step 3: Sign into Azure Acount

Log into your Azure account using the Azure CLI:

```bash
az login
```

### Step 4: Create Azure Resources

Navigate to the infra directory and run the script to create the necessary Azure resources:

```bash
cd infra && ./create_infrastructure.sh
```
**What This Does**: 
- A Resource Group is built containing Speech Services, Language Understanding, and Translator resources.
- A Key Vault is also created to securely store all essential keys and endpoint values.

### Step 5: Encrypt and Secure Secret Data

Navigate back to root directory and run the script to save and encrypt all secret data locally:

```bash
cd .. && python -m configuration.manage_secrets
```

### Step 6: Train CLU Model

Start the training session for your Conversation Language Understanding (CLU) model:

```bash
python -m training.begin_training_session
```
After training and deploying is complete, you can view your trained model at: https://language.cognitive.azure.com/home

</details>

## Usage
1. Run the program: `python main.py`
2. Wait for the startup sound to play, indicating that the assistant is now listening for input
3. Interact with the assistant by speaking

## Supported Packages
Packages come with prebuilt commands.
Intent recognition is done using your trained CLU model, allowing for versatile command phrasing.

<details>
<summary><b>Basic Package</b></summary>

#### Control Behavior
| Command | Response |
| ------- | -------- |
| Mute | Mutes the agent's responses |
| Unmute | Unmutes the agent's responses |
| Pause | Pauses all of the agent's functionalities |
| Exit | Terminates the program |
#### Personalization
| Command | Response |
| ------- | -------- |
| Change language to {language} | Changes the language of the agent to {language} |
| Change gender to {gender} | Changes the gender of the agent to {gender} |
| Change role to {role} | Changes the role of the agent to {role} |
| Change voice | Changes the agent's voice |

</details>

<details>
<summary><b>Virtual Assistant Package</b> (includes Basic)</summary>

#### Weather Retrieval
| Command | Response |
| ------- | -------- |
| What is the weather in {location} | Provides the current temperature in {location} |
#### Speech Translation
| Command | Response |
| ------- | -------- |
| Translate {speech} into {language} | Translates {speech} into {language} |
#### Control Lights
| Command | Response |
| ------- | -------- |
| Turn lights {off/on} | Turns the lights {off/on} |
| Change light color to {color} | Changes the light color to {color} |
#### Control Music 
| Command | Response |
| ------- | -------- |
| Play {song} | Plays {song} |
| Pause song | Pauses song |
| Play next song | Plays next song |
| Lower volume | Lowers volume of song playing by 10% |
| Raise volume | Raises volume of song playing by 10% |
#### Set Alarm
| Command | Response |
| ------- | -------- |
| Set an alarm for {day and time} | Sets an alarm for {day and time} |
#### Set Reminder
| Command | Response |
| ------- | -------- |
| Set a reminder for {day and time} to do {reminder} | Sets a reminder for {day and time} to do {reminder} |
#### Set Timer
| Command | Response |
| ------- | -------- |
| Set a timer for {time} {metric} | Sets a timer for {time} {metric} |
#### News Retrieval 
| Command | Response |
| ------- | -------- |
| Give me the news | A summary of the current top news stories (summarized using GPT) |
#### Web Browsing
| Command | Response |
| ------- | -------- |
| Open {website} | Opens the specified {website} |
| Search {speech} | Conducts a Google search for {speech} |
| Search youtube for {speech} | Conducts a YouTube search for {speech} |

</details>

Note: If a command is given that is not included in the above packages, a response will be given using GPT.
   
 ## Supported Languages
 Arabic, English (Australia, Ireland, UK, USA), Finnish, French, German, Hindi, Korean, Mandarin, Russian, Spanish
