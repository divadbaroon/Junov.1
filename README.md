# Juno

Customize, train, and deploy adaptive and intelligent conversational entities. Integrated with state-of-the-art AI technologies, Juno offers a modular, adaptable, and versatile solution for a wide range of use cases.

<details>
<summary><b>Key Features</b></summary>

### Cutting-Edge AI Integration

- Uses Azure [Speech Services](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/) for speech recognition. 
- Uses Azure  [CLU](https://learn.microsoft.com/en-us/azure/ai-services/language-service/conversational-language-understanding/overview) for intent recognition.
- Employs OpenAI's [GPT-3.5-Turbo](https://platform.openai.com/docs/models) for dynamic, human-like interactions.
- Leverages [Elevenlabs](https://docs.elevenlabs.io/welcome/introduction) for realistic human-sounding text-to-speech.


Note: Integrations will be continuously refined as better solutions become available.

### Highly Customizable

- **Packages**: Define custom commands, guiding entity behavior based on user input. See the [packages](#packages) section for more information.
- **Profiles**: Determine how the entity interacts with users. See the [profiles](#profiles) section for more information.
- **Custom Voices**: Elevenlabs supports the creation and usage of custom voices. With a five-minute audio file of a person speaking, a life-like voice can be created for Juno to use. See [Elevenlabs](https://elevenlabs.io/voice-lab) for more information.
- **Fine-Tune GPT**: Tailor GPT-3.5-Turbo's responses to your specific use-case by fine-tuning the model with training data. See /training/gpt_training_data for example training data.
  
**Tip**: You can effortlessly design profiles, craft custom voices, and fine-tune GPT directly through Juno's GUI. See the [Graphical User Interface](#graphical-user-interface) section for more information.

</details>

## Requirements
- Azure account and subscription
- Python 3.x
- Terraform 1.4.x

## Installation Guide

Execute all commands from the root directory of the project.

<details>
<summary><b>Expand to view steps </b></summary>

### Step 1: Install Required Packages

Run the following command to install the necessary packages:

```bash
pip install -r requirements.txt
```

### Step 2: Customize Configuration

Open the secret configuration file in your text editor for customization:

```bash
code configuration/config.yaml
```
Update the file with your personal settings and save it.

### Step 3: Sign into Azure Account

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
- Creates a Resource Group containing a Speech Service, Language Understanding, and Translator resource.
- Creates a Key Vault containing all necessary API keys and endpoints.

   **Note**: To destroy the created Azure resources run:
   ```bash
   cd infra && ./destroy_infrastructure.sh
   ```

### Step 5: Encrypt and Secure Secret Data

Navigate back to root directory and run the script to save and encrypt all secret data locally:

```bash
cd .. && python -m configuration.manage_secrets
```

### Step 6: Train CLU Model

Start the training session for your Conversation Language Understanding (CLU) model using the provided training data
located within 'training/virtual_assitant_training_data':

```bash
python -m training.begin_training_session
```
After training and deploying is complete, you can view your trained model at: https://language.cognitive.azure.com/home

### Step 7: Fine-tune GPT (Optional)

Begin a fine-tuning session for GPT using the provided training data located within 'training/gpt_training_data':

```bash
python -m training.begin_gpt_training_session
```

</details>

## Usage
1. Run the program: `python main.py`
2. Wait for the startup sound to play, indicating that the assistant is now listening for input
3. Interact with the assistant by speaking

## Packages
Used to provide Juno with specialized commands and responses. 
Training data located within /training is used to train an Azure CLU model to precisely detect intent for command execution. See /training for more information

<details>
<summary><b>Basic Package</b></summary>

#### Control Behavior
| Input | Response | Action |
| ------- | -------- | -------- |
| Mute  | I am now muted | Mutes responses | 
| Unmute | I am not unmuted | Unmutes responses |
| Pause | Pausing |  Pauses functionalities |
| Unpause | Unpaused |  Resumes functionalities |
| Exit | Exiting, goodbye! |  Terminates program |
#### Personalization
| Input | Response | Action |
| ------- | -------- | -------- |
| Change your language to {language} | Changing language to {language} | Changes language |
| Change your gender to {gender} | Changing gender to {gender} | Changes gender |
| Change your persona to {role} | Changing persona to {persona} | Changes persona |
| Change voice | I have changed my voice | Changes voice |

</details>

<details>
<summary><b>Virtual Assistant Package</b> (includes Basic)</summary>

#### Weather Retrieval
| Input | Response | Action |
| ------- | -------- | -------- |
| What is the weather in {location} | The weather in {location} is {temperature} degrees. | Fetches temperature via OpenWeatherMap API |
#### Speech Translation
| Input | Response | Action |
| ------- | -------- | -------- |
| Translate {speech} into {language} | {translated_speech} |  Uses Azure for speech translation |
#### Control Lights
| Input | Response | Action |
| ------- | -------- | -------- |
| Turn lights {off/on} | None | Controls smart LED lights |
| Change light color to {color} | None | Changes light color |
#### Control Music 
| Input | Response | Action |
| ------- | -------- | -------- |
| Play {song} | None |  Plays song via Spotify API |
| Pause song | None |  Pauses song via Spotify API |
| Play next song | None |  Plays next song via Spotify API |
| Lower volume | None | Decreases volume by 10% |
| Raise volume | None | Increases volume by 10% |
#### Set Alarm
| Input | Response | Action |
| ------- | -------- | -------- |
| Set an alarm for {day and time} | Setting an alarm for {day and time} | Sets an alarm |
#### Set Reminder
| Input | Response | Action |
| ------- | -------- | -------- |
| Set a reminder for {day and time} to do {reminder} | Setting a reminder | Sets a reminder for {day and time} to do {reminder} |
#### Set Timer
| Input | Response | Action |
| ------- | -------- | -------- |
| Set a timer for {time} {metric} | Setting a timer for {time} {metric} | Sets a timer |
#### News Retrieval 
| Input | Response | Action |
| ------- | -------- | -------- |
| Give me the news | Sure here is what's going on in the world. {Gives a summary of the top 3 news articles (using a fine-tuned GPT-3.5-turbo model | Fetches top news headlines via News API |
#### Web Browsing
| Input | Response | Action |
| ------- | -------- | -------- |
| Open {website} | Opening {website} |  Opens website |
| Search {speech} | Searching for {speech} |  Google search |
| Search youtube for {speech} | Searching Youtube for {speech} | Searches YouTube |

</details>

## Profiles
Used to customize the behavior of Juno, shaping its interactions based on specific users, technologies, and desired persona traits.

### The following attribute make up a profile:

<details>
<summary><b>Entity Attributes</b></summary>

| Attribute  | Example Value  | Description |
| :--------- | :------------ | :---------- |
| `name`     | barack obama  | The name of the entity |
| `gender`   | male          | Gender of the entity |
| `language` | english       | Language entity speaks in (Refer to documentation for available languages) |
| `personality` | friendly   | Describes the overall temperament of the entity |
| `persona`  | barack obama  | The entity will act as if they are this persona |
| `prompt`   | you are an assistant designed to concisely help the user with their queries | Prompt used to query GPT |
| `role`     | assistant     | Role of the entity |

</details>

<details>
<summary><b>System Attributes</b></summary>

| Attribute               | Example Value   | Description |
| :----------------------- | :-------------- | :---------- |
| `gpt_model`              | gpt-3.5-turbo   | Model used for generating responses (Fine-tuning recommended. See /training) |
| `package`                | virtual_assistant | Optional package for added functionalities. See [packages](#packages) for more information |
| `startup_sound`          | true           | Whether to play a startup sound |
| `voice_name`             | barack obama   | Voice used for text-to-speech. In this example, I am using a custom-made voice modeled after Barack Obama, created using Elevenlabs |
| `text_to_speech_engine`  | elevenlabs     | Engine used for text-to-speech (e.g., Elevenlabs or Azure) |
| `voice_recognition_engine` | azure        | Engine used for voice recognition |

</details>

<details>
<summary><b>User Attributes</b></summary>

| Attribute   | Example Value | Description |
| :----------- | :------------ | :---------- |
| `user_name`  | james          | Name of the user interacting with the entity |
| `user_gender`| male         | Gender of the user |
| `user_age`   | 22          | Age of the user |

</details>

<details>
<summary><b>Example Profile</b></summary>
   
```yaml
entity:
  name: barack obama
  gender: male
  language: english 
  personality: friendly
  persona: barack obama 
  prompt: you are an assistant designed to concisely help the user with their queries 
  role: assistant  
system:
  gpt_model: gpt-3.5-turbo 
  package: virtual_assistant 
  startup_sound: true 
  voice_name: barack obama 
  text_to_speech_engine: elevenlabs 
  voice_recognition_engine: azure 
user:
  user_name: null  
  user_gender: null   
  user_age: null
```
</details>

## Graphical User Interface
Juno supports a user-friendly graphical interface to easily customize and personalize Juno

To open the GUI, run the following command from root:
```bash
streamlit run configurator.py
```

 ## Supported Languages
 Arabic, English (Australia, Ireland, UK, USA), Finnish, French, German, Hindi, Korean, Mandarin, Russian, Spanish
