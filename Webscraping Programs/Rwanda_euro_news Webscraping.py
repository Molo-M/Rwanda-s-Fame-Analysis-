from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

url = []
name = []
year = []
category = []

page = 1
stop_page = 14

website_page = 'https://www.euronews.com/search?query=Rwanda'

while True:

    html_text = requests.get(website_page).text

    soup = BeautifulSoup(html_text, 'lxml')

    news = soup.find('div', class_='o-block-listing__articles')
    articles = news.find_all('article')

    for article in articles:
        article_name = article.find('a', rel='bookmark').text.strip()
        name.append(article_name)

        article_url = article.find('a', rel='bookmark')['href']
        link = 'https://www.euronews.com' + article_url
        url.append(link)

        dates = article.find('time').text.strip()
        dates = dates.split('/')
        date = int(dates[-1])
        year.append(date)

        article_category = article.find('a', {'data-event': 'article-label'})
        article_category = article_category.find('span').text.strip()
        category.append(article_category)

    print(f'Page {page} finished \n')
    page += 1

    next_page = soup.find('a', class_='c-paginator__text c-next')
    
    if next_page is not None:
        website_page = 'https://www.euronews.com' + next_page['href']
    else:
        break

news_dict = {'Name': name, 'Category': category, 'Year': year, 'URL': url}
df = pd.DataFrame(news_dict)
print(df)
# df.to_csv(r'C:\Users\HP\PycharmProjects\pythonProject' + '\\Rwanda_Euro_News.csv', index=False)
