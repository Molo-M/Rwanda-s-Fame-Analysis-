# Import useful libraries
import praw as pr
import pandas as pd
from datetime import datetime

# authorization for reddit api
user_agent = 'Scraper 1.0 by /u/python_for_fun'
reddit = pr.Reddit(client_id='**************', client_secret='**************',
                   user_agent=user_agent)

name = list()
link = list()
year = list()
number = 0

# Begin scraping the information
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

# save file to local pc
df.to_csv(r'C:\Users\HP\PycharmProjects\pythonProject' + '\\Rwanda_Reddit_Data.csv', index=False)
