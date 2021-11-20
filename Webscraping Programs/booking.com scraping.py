import pandas as pd
import numpy as np
from selenium import webdriver
import time

booking_name = []
number_of_reviews = []
area = []
link = []
scores = []
page = 1
stop_number = 13

webpage = 'https://www.booking.com/searchresults.html?label=gen173nr-' \
          '1FCAEoggI46AdIM1gEaMMBiAEBmAExuAEXyAEM2AEB6AEB-AECiAIBqAIDuAL_8reMBsACAdICJDIzMGVhYzI2LTA4NWYtNGIzOS0' \
          '5ZTBjLTZlNWI4ZThmOWM4MNgCBeACAQ&sid=87d75aca03e64e797d5f059bc0e38b2f&sb=1&sb_lp=1&src=index&src_elem=sb&' \
          'error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaMMBiAEBmAEx' \
          'uAEXyAEM2AEB6AEB-AECiAIBqAIDuAL_8reMBsACAdICJDIzMGVhYzI2LTA4NWYtNGIzOS05ZTBjLTZlNWI4ZThmOWM4MNgCBeACAQ%3B' \
          'sid%3D87d75aca03e64e797d5f059bc0e38b2f%3Bsb_price_type%3Dtotal%3Bsig%3Dv1TopEUQ8K%26%3B&ss=rwanda&is_' \
          'ski_area=0&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&n' \
          'o_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=rwanda&search_pageview_id=4d2e257fae470039'


# os.environ['PATH'] += r'C:\Selenium Drivers'
driver = webdriver.Chrome(executable_path='/Selenium Drivers/chromedriver.exe')
time.sleep(10)

driver.get(webpage)
while True:
    # driver.implicitly_wait(5)

    # property name
    names = driver.find_elements_by_css_selector("div[data-testid='title']")

    # location
    loc = driver.find_elements_by_css_selector("span[data-testid='address']")

    # url of property
    url = driver.find_elements_by_css_selector("a[data-testid='title-link']")

    # parse the property info
    for i in range(len(names)):
        booking_name.append(names[i].text)
        area.append(loc[i].text)
        link.append(url[i].get_attribute('href'))
    print('properties')

    data = driver.find_elements_by_css_selector("div[data-testid='property-card']")

    # parse the review and score number
    for properties in data:
        # number of reviews
        try:
            reviews = properties.find_element_by_css_selector("div[class='_4abc4c3d5 _1e6021d2f _fb3ba087b _6e869d6e0']")
            reviews = reviews.text.split()
            reviews = reviews[0].split(',')
            reviews = ''.join(reviews)
            number_of_reviews.append(int(reviews))
        except:
            number_of_reviews.append(np.nan)

        # score
        try:
            score = properties.find_element_by_css_selector("div[class='_9c5f726ff bd528f9ea6']")
            scores.append(float(score.text))
        except:
            scores.append(np.nan)

        print('------------')
    print(f'page {page} finished!!  \n')

    page += 1
    if page == stop_number:
        print(f'Done. Last name on page is {booking_name[-1]}')
        break

    # next page
    button = driver.find_element_by_css_selector("button[aria-label='Next page'")
    button.click()
    time.sleep(10)

    webpage = driver.current_url
driver.quit()

# create csv file:
booking_dict = {'Name': booking_name, 'Location': area, 'Reviews': number_of_reviews, 'Score': scores, 'URL': link}
df = pd.DataFrame(booking_dict)
print(df)

# df.to_csv(r'C:\Users\HP\PycharmProjects\pythonProject' + '\\Rwanda booking.com.csv', index=False)

