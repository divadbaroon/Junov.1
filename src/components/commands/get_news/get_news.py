import requests   

class GetNews():
	
	def __init__(self, ask_gpt:object, api_keys):
		self.query_params = {
		"source": "bbc-news",
		"sortBy": "top",
		"apiKey": api_keys['news_key']
		}
		self.main_url = " https://newsapi.org/v1/articles"

		# used to summarize articles
		self.gpt = ask_gpt
	
	def get_current_news(self, number_of_articles:int=3) -> dict:
		 # fetching data in json format
		data = requests.get(self.main_url, params=self.query_params)
		open_bbc_page = data.json()
	
		# getting all articles in a string article
		articles = open_bbc_page["articles"]
	
		# will contain all trending news titles with descriptions
		information = {}

		for i in range(number_of_articles): 
			information[f"article {i + 1}"] = {"title": articles[i]["title"], "description": articles[i]["description"]}
   
		response = self.gpt.ask_GPT(speech=f'Provide a summary of the daily news with these articles: {information}', model='gpt-4', manual_request=True)

		return response
