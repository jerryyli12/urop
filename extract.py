from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class element_has_options(object):
    def __init__(self, locator):
        self.locator = locator
    
    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        opts = element.find_elements_by_tag_name('option')
        if len(opts) > 1:
            return element
        return False


driver = webdriver.Chrome()
driver.get('https://msc.fema.gov/portal/advanceSearch')

try:
    _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'selstate'))
    )

    select_state = Select(driver.find_element_by_id('selstate'))
    select_state.select_by_visible_text('FLORIDA')

    _ = WebDriverWait(driver, 10).until(
        element_has_options((By.ID, 'selcounty'))
    )

    select_county = Select(driver.find_element_by_id('selcounty'))
    for county_option in select_county.options:
        if county_option.get_attribute('value') != 'none':
            county_option.click()
            _ = WebDriverWait(driver, 10).until(
                element_has_options((By.ID, 'selcommunity'))
            )

            select_community = Select(driver.find_element_by_id('selcommunity'))
            str_match = county_option.get_attribute('text') + ' ALL JURISDICTIONS'
            select_community.select_by_visible_text(str_match)

            driver.find_element_by_id('mainSearch').click()
            _ = WebDriverWait(driver, 10).until(
                EC.visibility_of(driver.find_element_by_class_name('searchresults'))
            )

finally:
    driver.quit()

# state_element = driver.find_element_by_id('selstate')
# state_options = state_element.find_elements_by_tag_name('option')
# for option in state_options:
#     if option.get_attribute('text') == 'FLORIDA':
#         option.click()
#         time.sleep(0.1)

# fails = 0

# county_element = driver.find_element_by_id('selcounty')
# county_options = county_element.find_elements_by_tag_name('option')
# for option in county_options:
#     if option.get_attribute('value') != 'none':
#         # print(option.get_attribute('value'),option.get_attribute('text'), '---------------')
#         option.click()
#         time.sleep(3)

#         str_match = option.get_attribute('text') + ' ALL JURISDICTIONS'
#         comm_found = False

#         community_element = driver.find_element_by_id('selcommunity')
#         community_options = community_element.find_elements_by_tag_name('option')
#         for community_option in community_options:
#             # print(community_option.get_attribute('text'))
#             if community_option.get_attribute('text') == str_match:
#                 comm_found = True
#                 community_option.click()
#                 break
        
#         if not comm_found:
#             fails += 1
#         else:


# print(fails)

# select_state = Select(driver.find_element_by_id('selstate'))
# select_state.select_by_visible_text('FLORIDA')
# time.sleep(3)

# select_county = Select(driver.find_element_by_id('selcounty'))
# for county_option in select_county.options:
#     if county_option.get_attribute('value') != 'none':
#         county_option.click()
#         time.sleep(3)

#         select_community = Select(driver.find_element_by_id('selcommunity'))
#         str_match = county_option.get_attribute('text') + ' ALL JURISDICTIONS'
#         select_community.select_by_visible_text(str_match)

#         driver.find_element_by_id('mainSearch').click()

            

