import praw as pr
import pandas as pd
from datetime import datetime

user_agent = 'Scraper 1.0 by /u/python_for_fun'
reddit = pr.Reddit(client_id='80wTfrz5Tr1JooibGrOU6g', client_secret='L09Cc94-y1MigcafPnn_9XSFxo42Vw',
                   user_agent=user_agent)

name = list()
link = list()
year = list()
number = 0

for submission in reddit.subreddit('Rwanda').new(limit=None):
    # print(submission.title)
    name.append(submission.title)
    # print(submission.url)
    link.append(submission.url)
    timestamp = datetime.fromtimestamp(submission.created)
    # print(timestamp)
    year.append(timestamp)
    number += 1
    print('----------')

print(number)

# create csv file:
reddit_dict = {'Title': name, 'Year': year, 'URL': link}
df = pd.DataFrame(reddit_dict)
print(df)

# df.to_csv(r'C:\Users\HP\PycharmProjects\pythonProject' + '\\Rwanda_Reddit_Data.csv', index=False)
