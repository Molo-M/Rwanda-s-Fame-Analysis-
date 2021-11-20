from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

year = []
url = []
name = []
article_category = []

page = 1
stop_number = 11

website_page = 'https://www.aljazeera.com/search/rwanda'

while True:

    html_text = requests.get(website_page).text

    soup = BeautifulSoup(html_text, 'lxml')

    news = soup.find('div', class_='l-col l-col--8')
    articles = news.find_all('article')

    for article in articles:
        article_url = article.find('a')
        article_url = article_url['href']
        url.append(article_url)
        # print(article_url)

        article_title = article.find('span').text
        name.append(article_title)
        print(article_title)

        # article date and categories
        html_article = requests.get(article_url).text

        parsed = BeautifulSoup(html_article, 'lxml')

        # article
        article_dates = parsed.find('div', class_='date-simple css-1yjq2zp').text
        if article_dates is not None:
            dates = article_dates.split()
            date = int(dates[-1])
            year.append(date)
            # print(date)
        else:
            year.append(2021)
            print(article_url)

        # category
        article_categories = parsed.find('div', class_='topics')
        if article_categories is not None:
            category = article_categories.find('a').text
            article_category.append(category)
            # print(category)
        else:
            article_category.append(np.nan)
            # print(np.nan)
        # print('---------------------------------------------------')

    print(f'page {page} finished' + '\n')
    page += 1

    # next page
    next_page = soup.find('a', eventtarget='Next')
    website_page = 'https://www.aljazeera.com' + next_page['href']
    # print(website_page)

    if page == stop_number:
        print(website_page)
        break

# create csv table
article_dict = {'Name': name, 'Category': article_category, 'Year': year, 'URL': url}
df = pd.DataFrame(article_dict)
print(df)
# df.to_csv(r'C:\Users\HP\PycharmProjects\pythonProject' + '\\Rwanda_Aljazeera_Data.csv', index=False)

