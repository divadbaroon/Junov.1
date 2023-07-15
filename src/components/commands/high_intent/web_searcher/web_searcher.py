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