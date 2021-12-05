import pandas as pd
import numpy as np
from selenium import webdriver
import time

property_name = []
number_of_reviews = []
area = []
provinces_area = []
link = []
property_rating = []
page = 1
stop_number = 50

webpage = 'https://www.tripadvisor.com/Hotels-g293828-Rwanda-Hotels.html'

driver = webdriver.Chrome(executable_path='/Selenium Drivers/chromedriver.exe')
time.sleep(15)

driver.get(webpage)
time.sleep(15)

while True:
    item = driver.find_elements_by_css_selector("a[class='property_title prominent ']")
    lists = driver.find_elements_by_css_selector("div[class='prw_rup prw_meta_hsx_responsive_listing ui_section "
                                                 "listItem']")

    for i in range(len(item)):
        try:
            # property name
            property_name.append(item[i].text)

            # url
            url = item[i].get_attribute('href').split('-')
            link.append(item[i].get_attribute('href'))

        except:
            print('Name: ', property_name[-1])
            print(f'Problem on page {page}. Stopping program......')
            quit()

        # Get locations
        location = url[-1].split('.')
        location = location[0].split('_')
        province = ' '.join(location[-2:])
        provinces_area.append(province.strip())

        location = location[:-2]
        try:
            area.append(location[0])
        except IndexError:
            area.append(np.nan)

        # number of reviews
        try:
            reviews = lists[i].find_element_by_css_selector("a[class='review_count']")
            review = reviews.text.split()
            number_of_reviews.append(review[0])
        except:
            number_of_reviews.append(np.nan)

        # rating
        try:
            ratings = lists[i].find_element_by_css_selector("a[data-clicksource='BubbleRating']")
            rating = ratings.get_attribute('alt')
            rating = rating.split()
            property_rating.append(rating[0])
        except:
            property_rating.append(np.nan)

    # MAKE SURE PAGE IS NOT REPEATED:
    if page != 1:

        current_page = driver.find_element_by_css_selector("span[class='pageNum current current ']").text
    else:
        current_page = '1'
    if page > int(current_page):

        print(f'Page {int(current_page)} has repeated!!!')

        # delete repeated values:
        delete_val = len(item)
        del property_name[(-delete_val):]
        del property_rating[(-delete_val):]
        del link[(-delete_val):]
        del area[(-delete_val):]
        del provinces_area[(-delete_val):]
        del number_of_reviews[(-delete_val):]

        # Go to previous page
        previous = driver.find_element_by_css_selector("span[class='nav previous ui_button secondary']")
        previous.click()
        print('----------')
        time.sleep(30)

        # next page
        button = driver.find_element_by_css_selector(f"span[data-page-number='{str(page)}']")
        button.click()
        print('----------')
        time.sleep(30)

        # button = driver.find_element_by_css_selector("span[class='nav next ui_button primary']")
        # button.click()
        # print('----------')
        # time.sleep(30)

        continue

    print(f'Page {page} finished!!')
    page += 1

    # next page
    try:
        button = driver.find_element_by_css_selector("span[class='nav next ui_button primary']")
        button.click()
        time.sleep(30)
    except:
        driver.quit()
        break

# create csv file:
tripadvisor_dict = {'Name': property_name, 'Location': area, 'Province': provinces_area, 'Reviews': number_of_reviews,
                    'Rating(out of 5)': property_rating, 'URL': link}

df = pd.DataFrame(tripadvisor_dict)
print(df)

df.to_csv(r'C:\Users\HP\PycharmProjects\pythonProject' + '\\Rwanda tripadvisor.csv', index=False)
