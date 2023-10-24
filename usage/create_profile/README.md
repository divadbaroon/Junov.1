# How to Create a Profile
Profiles are used to customize the behavior of Juno, shaping its interactions based on specific users, technologies, and desired persona traits.

<<<<<<< HEAD
1. Run the following command from root to open Juno's GUI.
```Bash
streamlit run configurator.py
```

2. Naviagate to the "Create Profile" page and Configure the profile to your liking, then hit "Create".

3. Run the program (the most recently created or updated profile is used by defualt)
```Bash
=======
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
>>>>>>> 5239207c93c78e4b4c7a897f7a2676a68add6d1d
python main.py
```

