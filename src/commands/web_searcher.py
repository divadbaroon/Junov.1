import webbrowser
import urllib.parse

class WebSearcher:
	"""
	A class that contains methods for opening a desired website, 
	performing a google search, and performing a youtube search.
	"""
				
	def open_website(self, website: str):
		"""
		Opens the specified website in a new browser window.
		:param website: (str) the website to open
		"""
		webbrowser.open(f"https://www.{website}.com")
		
		return f'Opening {website}.com'

	def search_google(self, search_request: str):
		"""
		Performs a google search for a given query
		:param search_request: (str) the google search request
		"""
		webbrowser.open(f"https://www.google.com/search?q={search_request}")
				
		return f'Searching google for {search_request}'
			
	def search_youtube(self, search_request: str):
		"""
		Performs a youtube search for a given query
		:param search_request: (str) the youtube search request
		"""
		# Encode the search request to be url friendly
		query = urllib.parse.quote(search_request)
		webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
				
		return f'Searching youtube for {search_request}'