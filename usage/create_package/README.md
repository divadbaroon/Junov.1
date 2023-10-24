# How to Create a Package
Packages are used to provide Juno with specialized commands and responses. Training data located within /training is used to train an Azure CLU model to precisely detect intent for command execution. See /training for more information

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

## Preparing your directories

### 1. Create a subdirectory within the /training directory for the training data. Name it appropriately.

For this example the command will be apart of the virtual_assistant package:
```Bash
mkdir /training/virtual_assistant/search_google
```

If creating your own package, create the package as a subfolder in the training directory such as:
```Bash
mkdir /training/your_package_name
```

### 2. Create the necessary JSON files for the CLU Model. The CLU Model trains a model to detect intent.

For example:
```Bash
cd /training/virtual_assistant/search_google
mkdir entities.json, intents.json, utterances.json
```

## Preparing your data

- In the 'entities.json' file, provide a name to represent the name for the desired information you 
  want extracted from the user's speech. 

In this example, it's the user's Google query:
```json
[
  {
    "category": "google_query"
  }
]
```

- In the 'intents.json' file, provide a name for your command.

Since in this case we are searching google it is called "search_google":
```json
{
  "intents": [
    {
      "category": "Search_Google"
    }
  ]
}
```

- In the 'utterances.json' file provide sample utterances to be used for training. Enter utterances that you want to trigger a command.
It's recommended to have at least 15 utterances, but more is always better. For brevity, only a few samples are shown 

- Location of the desired argument is also requried
- "category" use the name used in 'entities.json' file. This param represents the name we assigned the arg earlier
- "offset" represents the starting position of the desired information
- "length" represents the length of your 

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
    }
]
```

Additional examples can be found in the /training directory.

## Training your model
From the root directory run the following command and enter the name of the package in which you would like to train:
```Bash
python -m training.begin_training_session
```

## Use The Command
Now, run the main program to see the command in action:
```Bash
python main.py
```
