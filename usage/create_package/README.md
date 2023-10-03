# How to Create a Package
Packages are used to store folder for custom commands that GPT cannot do such as interacting with the browser, executing commands using cli, interacting with spotify, etc. 
In order to create a package a script needs to be created to be executed and training data needs to be provied to train the CLU model to detect the 
user's intent to execute the command

## Example
For this example a command called web_searcher will be created as apart of the virtual_assistant package.

### Command

For this example a python file is being used to seach the web.

This script in this example recieves a query from the user and utilizes the webbrowser library to open the query. A response as string to be verbalized is then returned. Text-to-speech is perform on all text returned from commands.

```Python
import webbrowser
import urllib.parse

class WebSearcher:
	"""
	A class that contains methods for opening a desired website, 
	performing a google search, and performing a youtube search.
	"""
				
	def open_website(self, website: str) -> str:
		"""
		Opens the specified website in a new browser window.
		"""
		webbrowser.open(f"https://www.{website}.com")
		
		return f'Opening {website}.com'

	def search_google(self, search_request: str) -> str:
		"""
		Performs a google search for a given query
		"""
		webbrowser.open(f"https://www.google.com/search?q={search_request}")
				
		return f'Searching google for {search_request}'
			
	def search_youtube(self, search_request: str) -> str:
		"""
		Performs a youtube search for a given query
		"""
		query = urllib.parse.quote(search_request)
		webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
				
		return f'Searching youtube for {search_request}'
```

### Training Data

1. Create a subdirectory within the '/training' directory to store the training data. Name it accordingly.

For example:
```Bash
'mkdir /training/search_google'
```

2. Create the necessary json files to be query to the CLU Model. The CLU Model is used for creating a trained model to detect intent

For example:
```Bash
cd 'mkdir /training/search_google'
mkdir entities.json, intents.json, utterances.json
```

The 'entities.json' file contains the desired information returned from the user's speech. In this example it the was the user's google query:
```json
[
  {
    "category": "google_query"
  }
]
```

The 'intents.json' file contains the name of the command which in this case was Search Google:
```json
{
  "intents": [
    {
      "category": "Search_Google"
    }
  ]
}
```

the 'utterances.json''' file contains the example utterances to be used for training:

It is recommended to have at least 15 utterances, however, the more the better
```json
[
    {
        "text": "google best pizza places in Chicago",
        "intent": "Search_Google", //name of command given in entities.json
        "entities": [
            {
                "category": "google_query", //name of arg given in entities.json
                "offset": 7, //where the arg starts
                "length": 28 //length of arg 
            }
        ]
    },
    {
        "text": "google how to get better at chess",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 7,
                "length": 26
            }
        ]
    },
    {
        "text": "google pizza recipes",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 7,
                "length": 13
            }
        ]
    },
    {
        "text": "google how to solve a rubik's cube",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 7,
                "length": 27
            }
        ]
    },
    {
        "text": "google who is the president",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 7,
                "length": 20
            }
        ]
    },
    {
        "text": "search the closest barber shop",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 7,
                "length": 23
            }
        ]
    },
    {
        "text": "search for funny cat videos",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 7,
                "length": 20
            }
        ]
    },
    {
        "text": "search the fermi paradox",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 7,
                "length": 17
            }
        ]
    },
    {
        "text": "search covid-19",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 7,
                "length": 8
            }
        ]
    },
    {
        "text": "search google for information on Taiwan",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 14,
                "length": 25
            }
        ]
    },
    {
        "text": "Can you Google how long to let clothes air dry",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 15,
                "length": 31
            }
        ]
    },
    {
        "text": "can you google calculus",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 15,
                "length": 8
            }
        ]
    },
    {
        "text": "can you google information about mental health",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 15,
                "length": 31
            }
        ]
    },
    {
        "text": "can you google the moon landing",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 15,
                "length": 16
            }
        ]
    },
    {
        "text": "can you google how to get better at golf",
        "intent": "Search_Google",
        "entities": [
            {
                "category": "google_query",
                "offset": 15,
                "length": 25
            }
        ]
    }
]
```

Further examples can be be seen within the '/training' directory

## Train The Modle
From the root directory run the following command:
```Bash
python -m training.begin_training_session
```

The command will now be utilized within Juno
```Bash
python main.py
```