# import useful libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

website_page = 'https://www.bbc.co.uk/search?q=rwanda'

# Create information holders
name = list()
link = list()
year = list()
categories = list()
channel = list()

page_number = 1
stop_number = 29

# Begin scraping process
while True:

    html_text = requests.get(website_page).text

    soup = BeautifulSoup(html_text, 'lxml')

    news = soup.find('ul', spacing='responsive', role='list')
    articles = news.find_all('li')

    # start scraping page:
    for article in articles:

        # add name
        article_name = article.find('span').text
        name.append(article_name)
        # print(article_name)

        # add link
        article_link = article.find('a')
        link.append(article_link['href'])
        # print(article_link['href'])

        # add categories
        article_category = article.find_all('span', class_='ssrcss-8g95ls-MetadataSnippet ecn1o5v2')
        for category in article_category:
            # ARTICLE WITH 3 CATEGORIES:
            if len(article_category) == 3:
                # date:
                if category == article_category[0]:
                    dates = category.text
                    dates = dates.split()
                    try:
                        date = int(dates[-1])
                        year.append(date)
                        # print(date)
                    except ValueError:
                        date = 2021
                        year.append(date)
                        # print(date)

                # category:
                elif category == article_category[1] and article_category[1] != article_category[2]:
                    categories.append(category.text)
                    # print(category.text)

                # channel:
                elif category == article_category[2] and article_category[1] != article_category[2]:
                    channel.append(category.text)
                    # print(category.text)
                    # print('---------------------------------------------------------')

                # if channel and category are the same:
                elif article_category[1] == article_category[2] and category != article_category[0]:
                    categories.append(category.text)
                    channel.append(category.text)
                    # print(category.text)
                    # print(category.text)
                    break

            # ARTICLE WITH ONLY 2 CATEGORIES:
            else:
                if category == article_category[0]:
                    # date
                    year.append(2021)
                    # category:
                    categories.append(category.text)
                    # print(category.text)

                # channel:
                elif category == article_category[1]:
                    channel.append(category.text)
                    # print(category.text)

    print('finished: ', page_number)
    print('website:', website_page, 'finished')

    # next page button
    buttons = soup.find_all('div', class_='ssrcss-zhhf7y-PageButtonContainer e1b2sq420')
    for button in buttons:
        if button == buttons[-1]:
            page = button.find('a')
            website_page = 'https://www.bbc.co.uk' + page['href']

    page_number += 1

    if page_number > stop_number:
        break

print('page stop: ', page_number)

# create csv file:
news_dict = {'Name': name, 'Channel': channel, 'Category': categories, 'Year': year, 'URL': link}
df = pd.DataFrame(news_dict)
print(df)

# save file to local pc
df.to_csv(r'C:\Users\HP\PycharmProjects\pythonProject' + '\\Rwanda_BBC_Data.csv', index=False)
