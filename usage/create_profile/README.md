# How to Create a Profile
Profiles are used to personalize the bot by the providing the following params.

### Data

1. Create a subdirectory within the '/training' directory to store the training data. Name it accordingly.

    For example:
    ```Bash
    mkdir /profiles/profile_storage/default
    ```

2. Customize training data to your liking:

```yaml
interaction:
  current_language: english ## check documentation for available languages
  personality: friendly
  prompt: you are a virtual assistant ## prompt to be used by GPT
  role: assistant  
system:
  package: virtual_assistant ## or basic
  startup_sound: true ## or false
  voice_engine: elevenlabs ## or azure
  voice_name: Bella ## check documentation for available names
  voice_recognition_engine: azure # only azure available
user:
  gender: female 
  name: Juno
```

## Use the profile

1. example usage of new profile
```Bash
python -m usage.create_profile.create_new_profile
```

