# Juno 
A platform designed for effortless setup, training, and usage in creating intelligent text-to-speech based agents. Juno was designed to be modular, customizable, and extensible making it suitable for a wide range of use cases.

## Key Features 
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

## Requirements
- Azure account and subscription
- Python 3.x

## Installation
Run all commands from root directory
1. Install the required packages: `pip install -r requirements.txt`
2. Customize configuration: `code configuration/secrets/secret_config.yaml` 
3. Sign into your Azure account: `az login`
4. Create necessary Azure resources: `cd ./infra && ./infra/create_infrastructure.sh`
5. Encrypt and secure your configuration secrets: `cd .. && python configuration/encrypt_secrets`
6. Train LUIS model with training data: `python training/begin_training_session.py`

## Usage
1. Run the program: `python main.py`
2. Wait for the startup sound to play, indicating that the assistant is now listening for input
3. Interact with the assistant by speaking

## Supported Packages
Packages come with prebuilt commands.
Intent recognition is done using your trained LUIS model, allowing for versatile command phrasing.

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
   
 ## Supported Langauges
 Arabic, English (Australia, Ireland, UK, USA), Finnish, French, German, Hindi, Korean, Mandarin, Russian, Spanish
