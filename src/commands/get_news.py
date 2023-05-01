import requests

class GetNews:

    def get_articles(self, news_key, topic, language='en', page_size=20, sort_by='relevancy', from_date='2023-04-01'):
        
        url = 'https://newsapi.org/v2/everything'

        params = {
            'apiKey': news_key,
            'q': topic,
            'language': language,
            'pageSize': page_size,
            'sortBy': sort_by,
            'from': from_date
        }

        response = requests.get(url, params=params)
        
        news_data = response.json()
        
        descriptions = ['Here is some news on that topic:']

        # If the request was successful, return the first article's description
        if news_data and news_data['status'] == 'ok' and news_data['totalResults'] > 0:
            for i, article in enumerate(news_data['articles'], start=1):
                descriptions.append(f"Article {i} Description: {article['description']}")
            return descriptions
        else:
            return "Sorry, there was an error retrieving the news. Please try again later."