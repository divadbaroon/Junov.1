# How to Create a Profile
Profiles are used to customize the behavior of Juno, shaping its interactions based on specific users, technologies, and desired persona traits.

Note: Run all commands from root directory.

### Create a Profile

1. Open 'example_profile.yaml', edit the file to your liking, and save it.
    ```Bash
    code usage/create_profile/example_profile.yaml
    ```

2. Create your new profile.
    ```Bash
    python -m usage.create_profile.create_new_profile
    ```

   Note: this will set that profile as the current profile. To change your profile open master settings:
   ```Bash
    code src/utilities/settings/master_settings/master_settings.json
    ```

## Use the Profile

1. Run the program:
```Bash
python main.py
```

