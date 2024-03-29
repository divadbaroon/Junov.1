import requests   

class GetNews():
	
	def __init__(self, ask_gpt:object, api_keys:dict):
		self.query_params = {
		"source": "bbc-news",
		"sortBy": "top",
		"apiKey": api_keys['NEWS-API-KEY']
		}
		self.main_url = " https://newsapi.org/v1/articles"

		# using GPT to summarize articles
		self.gpt = ask_gpt
	
	def get_news(self, number_of_articles:int=3) -> dict:
		"""Returns the top news articles from BBC News."""
     
		 # fetching data in json format
		data = requests.get(self.main_url, params=self.query_params)
		open_bbc_page = data.json()
	
		# getting all articles in a string article
		articles = open_bbc_page["articles"]
	
		# will contain all trending news titles with descriptions
		information = {}

		for i in range(number_of_articles): 
			information[f"article {i + 1}"] = {"title": articles[i]["title"], "description": articles[i]["description"]}
   
		# using GPT to summarize articles 
		response = self.gpt.ask_GPT(speech=f'You are a virtual assistant tasked with providing a summary of the daily news given these news articles: {information}', model="ft:gpt-3.5-turbo-0613:personal:juno-test:82ZECb8b", manual_request=True, max_tokens=200)

		return response
