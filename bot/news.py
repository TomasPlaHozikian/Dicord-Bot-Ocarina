from newsapi import NewsApiClient

#news api class
class News:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key='your key')
        
    def get_news(self, message):
        all_articles = self.newsapi.get_everything(q=message, language='es', sort_by='relevancy')
        top_headlines = self.newsapi.get_top_headlines(q=message,
                                          language='es',
                                          country='ar')
        articles = all_articles["articles"]
        top_headlines = top_headlines["articles"]
        dict = {}
        texto = ""
        for article in articles:
            dict[article["title"]] = [article["description"], article["url"]]
        count = 0
        for key in dict:
            if count >= 2:
                break
            texto += f"{key}: {str(dict[key])[2:-2]}\n\n"
            count += 1
        return texto