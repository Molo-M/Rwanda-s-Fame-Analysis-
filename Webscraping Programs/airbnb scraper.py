import pandas as pd
import numpy as np
from selenium import webdriver
import time

property_name = []
number_of_reviews = []
area = []
link = []
property_rating = []
page = 1
stop_number = 16

webpage = 'https://www.airbnb.com/s/Rwanda/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_' \
          'dates%5B%5D=december&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_' \
          'type=calendar&query=Rwanda&place_id=ChIJ40A451SWwhkRA6HMyyawkHQ&source=structured_search_input_header&search' \
          '_type=autocomplete_click'

driver = webdriver.Chrome(executable_path='/Selenium Drivers/chromedriver.exe')
time.sleep(15)

driver.get(webpage)
time.sleep(150)

while True:
    # Begin scraping
    room_names = driver.find_elements_by_css_selector("meta[itemprop='name']")
    url = driver.find_elements_by_css_selector("meta[itemprop='url']")
    location = driver.find_elements_by_css_selector("div[class='_1xzimiid']")

    items = driver.find_elements_by_css_selector("div[class='_8ssblpx']")

    # Make sure page is scraping correctly
    current_page = driver.find_element_by_css_selector("button[aria-current='page']")
    current_page = int(current_page.text)
    if page > current_page:
        print(f'Page {int(current_page)} has repeated')
        pages = driver.find_elements_by_css_selector("a[class='_833p2h']")
        find_page = pages[2]
        find_page.click()
        continue

    elif len(room_names) != len(items):
        print(f'Lengths are not equal, on page {page}. Trying again.....')
        continue

    # Saving data collected
    for i in range(len(room_names)):
        # name
        property_name.append(room_names[i].get_attribute('content'))

        # URL
        link.append(url[i].get_attribute('content'))

        # location
        loc = location[i].text.split()
        loc = loc[-1]
        area.append(loc)

        try:
            customer_rating = items[i].find_element_by_css_selector("span[class='_18khxk1']")
            customers = customer_rating.get_attribute('aria-label').split(';')

            # Reviews
            reviews = customers[-1].split()
            reviews = reviews[0].strip()
            number_of_reviews.append(int(reviews))

            # Rating
            rating = customers[0].split()
            rating = rating[1]
            property_rating.append(float(rating))
        except:
            number_of_reviews.append(np.nan)
            property_rating.append(np.nan)

    print(f'Page {page} finished. Searching for next page...')

    page += 1
    if page == stop_number:
        break

    # Next page
    button = driver.find_element_by_css_selector("a[aria-label='Next']")
    button.click()

    time.sleep(30)

driver.quit()

# create csv file:
airbnb_dict = {'Name': property_name, 'Location': area, 'Reviews': number_of_reviews,
               'Rating(out of 5)': property_rating, 'URL': link}

df = pd.DataFrame(airbnb_dict)
print(df)

df.to_csv(r'C:\Users\HP\PycharmProjects\pythonProject' + '\\Rwanda airbnb.csv', index=False)
