# Juno

Customize, train, and deploy intelligent text-to-speech entities. Integrated with state-of-the-art AI technologies, Juno offers a modular, adaptable, and versatile solution for a wide range of use cases.

<details>
<summary><b>Key Features</b></summary>

### Advanced AI Integration

- Uses Azure [Speech Services](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/) for speech recognition. 
- Uses Azure  [CLU](https://learn.microsoft.com/en-us/azure/ai-services/language-service/conversational-language-understanding/overview) for intent recognition.
- Employs OpenAI's [GPT-3.5-Turbo](https://platform.openai.com/docs/models) for dynamic, human-like interactions.
- Leverages [Elevenlabs](https://docs.elevenlabs.io/welcome/introduction) for realistic sounding text-to-speech.


Note: Integrations will be continuously refined as better solutions become available.

### Highly Customizable

- **Packages**: Define custom commands, guiding entity behavior based on user input. See the [packages](https://github.com/divadbaroon/Juno#supported-packages) section for more information.
- **Profiles**: Determine how the entity interacts with users. See the [profiles](#profiles) section for more information.
- **Custom Voices**: Elevenlabs supports the creation and usage of cutom voices. See the [Elevenlabs](https://elevenlabs.io/voice-lab) for more information.
- **Fine-Tune GPT**: Tailor GPT-3.5-Turbo's responses to your specific needs by fine-tuning the model with training data. See /training/gpt_training_data for example training data.

### Comprehensive Conversational Abilities

- Trained on a vast dataset, ensuring adept handling of varied commands and prompts. Training data is located within /training.
- Maintains conversation history for context-aware responses.

</details>

## Requirements
- Azure account and subscription
- Python 3.x
- Terraform 1.4.x

## Installation Guide

Execute all commands from the root directory of the project.

<details>
<summary><b>Expand to view steps 🔽 </b></summary>

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
| Command | Response |
| ------- | -------- |
| Mute | Mutes the entity's responses |
| Unmute | Unmutes the entity's responses |
| Pause | Pauses all of the entity's functionalities |
| Unpause | Unpauses all of the entity's functionalities |
| Exit | Terminates the program |
#### Personalization
| Command | Response |
| ------- | -------- |
| Change language to {language} | Changes the language of the entity to {language} |
| Change gender to {gender} | Changes the gender of the entity to {gender} |
| Change role to {role} | Changes the role of the entity to {role} |
| Change voice | Changes the entity's voice |

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

See /usage for how to create and use your own packages.

## Profiles
Used to customize the behavior of Juno, shaping its interactions based on specific users, technologies, and desired persona traits.

<details>
<summary><b>Example Profile</b></summary>
   
```yaml
interaction:
  language: english ## see documentation for available languages
  personality: friendly
  persona: Obama ## entity will act as if they are this persona 
  prompt: you are a virtual assistant ## prompt to be used by GPT
  role: assistant  
system:
  package: virtual_assistant ## optional
  startup_sound: true ## optional
  voice_engine: elevenlabs ## or azure
  voice_name: Obama ## custom realistic sounding obama voice created using Elevenlabs. 
  voice_recognition_engine: azure # currently only azure available
user:
  gender: female 
  name: david   
```
</details>

See /usage for how to create and use your own profiles.
   
 ## Supported Languages
 Arabic, English (Australia, Ireland, UK, USA), Finnish, French, German, Hindi, Korean, Mandarin, Russian, Spanish
