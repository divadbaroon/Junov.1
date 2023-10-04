# How to Create a Package
Packages are used to store folders for custom commands that GPT cannot handle natively, such as interacting with a browser, executing CLI commands, interacting with Spotify, etc. To create a package, you need a script to be executed and training data for the CLU model to detect the user's intent to execute the command.

## Example
For this example, we'll create a command named web_searcher as part of the virtual_assistant package.

### Command
In this example, a Python script is used to search the web. This script receives a query from the user, uses the webbrowser library to process the query, and then returns a string response to be verbalized. All text returned from commands undergoes text-to-speech processing.

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

1. Create a subdirectory within the /training directory for the training data. Name it appropriately.

For this example the command will be apart of the virtual_assistant package:
```Bash
mkdir /training/virtual_assistant/search_google
```

If creating your own package, create the package as a subfolder in the training directory such as:
```Bash
mkdir /training/search_google
```

For example:
```Bash
cd 'mkdir /training/virtual_assistant/search_google'
mkdir entities.json, intents.json, utterances.json
```

'entities.json' contains the desired information extracted from the user's speech. In this example, it's the user's Google query:
```json
[
  {
    "category": "google_query"
  }
]
```

'intents.json' contains the name of the command, which in this case is 
```json
{
  "intents": [
    {
      "category": "Search_Google"
    }
  ]
}
```

'utterances.json' contains the sample utterances for training. It's recommended to have at least 15 utterances, but more is always better. For brevity, only a few samples are shown 
```json
[
    {
        "text": "google best pizza places in Chicago",
        "intent": "Search_Google", 
        "entities": [
            {
                "category": "google_query", 
                "offset": 7, 
                "length": 28 
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

Additional examples can be found in the /training directory.

## Train The Modle
From the root directory run the following command:
```Bash
python -m training.begin_training_session
```

## Use The Command
Now, you can run the main program to see the command in action:
```Bash
python main.py
```