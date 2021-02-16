from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlretrieve
import csv
import time
import os


class element_has_options(object):
    """
    Checks if the HTML element (probably be a form) has multiple elements with <option> tag.
    """
    def __init__(self, locator):
        self.locator = locator
    
    def __call__(self, driver):
        """
        Returns the list of elements with tag <option> or False if there is only one.
        """
        element = driver.find_element(*self.locator)
        opts = element.find_elements_by_tag_name('option')
        if len(opts) > 1:
            return element
        return False

# Load website
driver = webdriver.Chrome()
driver.get('https://msc.fema.gov/portal/advanceSearch')

outp = csv.writer(open('file_to_date.csv','a', newline=''), delimiter=',')

try:
    # Wait until website is loaded
    _ = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'selstate'))
    )

    # Select Florida from states dropdown
    select_state = Select(driver.find_element_by_id('selstate'))
    select_state.select_by_visible_text('FLORIDA')

    # Wait until county dropdown is loaded
    _ = WebDriverWait(driver, 120).until(
        element_has_options((By.ID, 'selcounty'))
    )

    # Loop through all counties
    select_county = Select(driver.find_element_by_id('selcounty'))
    for county_option in select_county.options:
        if county_option.get_attribute('value') != 'none':
            # Select county and wait until community dropdown is loaded
            county_option.click()
            _ = WebDriverWait(driver, 120).until(
                element_has_options((By.ID, 'selcommunity'))
            )

            county_name_lower = county_option.get_attribute('text').lower()
            outp_path = 'output/' + county_name_lower
            if os.path.isdir(outp_path):
                continue
            os.makedirs(outp_path, exist_ok=True)

            # Select ALL JURISDICTIONS community
            select_community = Select(driver.find_element_by_id('selcommunity'))
            str_match = county_option.get_attribute('text') + ' ALL JURISDICTIONS'
            select_community.select_by_visible_text(str_match)
            
            print(str_match)

            # Click search and wait until search results are loaded
            driver.find_element_by_id('mainSearch').click()
            _ = WebDriverWait(driver, 120).until(
                EC.visibility_of(driver.find_element_by_class_name('searchresults'))
            )

            # Open up the table
            table_loaded = True
            try:
                driver.find_element_by_id('eff_root').click()
                _ = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.ID, 'eff_lomc_root'))
                )
                driver.find_element_by_id('eff_lomc_root').click()
                _ = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.ID, 'eff_main_loma_root'))
                )
                driver.find_element_by_id('eff_main_loma_root').click()
                eff_loma_root_elt = driver.find_element_by_css_selector('div[aria-labelledby="eff_main_loma_root"]')
                _ = WebDriverWait(driver, 120).until(
                    EC.visibility_of(eff_loma_root_elt)
                )
            except Exception as e:
                table_loaded = False

            if table_loaded:
                prev_header = ''

                print(eff_loma_root_elt.find_element_by_class_name('dataTables_info').get_attribute('innerHTML'))

                while True:
                    eff_loma_list_elt = eff_loma_root_elt.find_element_by_id('eff_loma_list')
                    eff_loma_rows = eff_loma_list_elt.find_elements_by_css_selector('tr[role="row"]')

                    # Loop through all rows in table
                    for row in eff_loma_rows:
                        entries = row.find_elements_by_css_selector('td')
                        file_id = entries[0].get_attribute('innerHTML')
                        file_date = entries[1].get_attribute('innerHTML')
                        file_link = entries[2].find_element_by_css_selector('a').get_attribute('href')

                        act_link = 'https://map1.msc.fema.gov/data' + file_link[file_link.find('filepath') + 9 : file_link.find('.pdf') + 4]
                        # print(file_id, file_date, file_link)

                        # Download and write to csv
                        if int(file_date[-4:]) >= 2000:
                            urlretrieve(act_link, outp_path + '/' + file_id + '.pdf')
                            outp.writerow([file_id, file_date])

                    try:
                        # Click next to go to next page
                        next_button = eff_loma_root_elt.find_element_by_css_selector('.next:not(.disabled)')
                        next_button.click()
                        _ = WebDriverWait(driver, 120).until(
                            lambda dr: eff_loma_root_elt.find_element_by_class_name('dataTables_info').get_attribute('innerHTML') != prev_header
                        )
                        prev_header = eff_loma_root_elt.find_element_by_class_name('dataTables_info').get_attribute('innerHTML')
                        print(prev_header)

                    except NoSuchElementException as e:
                        break

            # Do again, but for historic    

            table_loaded = True
            try:
                driver.find_element_by_id('historic_root').click()
                _ = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.ID, 'historic_lomc_root'))
                )
                driver.find_element_by_id('historic_lomc_root').click()
                _ = WebDriverWait(driver, 120).until(
                    EC.element_to_be_clickable((By.ID, 'his_loma_root'))
                )
                driver.find_element_by_id('his_loma_root').click()
                his_loma_root_elt = driver.find_element_by_css_selector('div[aria-labelledby="his_loma_root"]')
                _ = WebDriverWait(driver, 120).until(
                    EC.visibility_of(his_loma_root_elt)
                )
            except Exception as e:
                table_loaded = False
            
            if table_loaded:
                prev_header = ''

                print(his_loma_root_elt.find_element_by_class_name('dataTables_info').get_attribute('innerHTML'))

                while True:
                    his_loma_list_elt = his_loma_root_elt.find_element_by_id('his_loma_list')
                    his_loma_rows = his_loma_list_elt.find_elements_by_css_selector('tr[role="row"]')

                    # Loop through all rows in table
                    for row in his_loma_rows:
                        entries = row.find_elements_by_css_selector('td')
                        file_id = entries[0].get_attribute('innerHTML')
                        file_date = entries[1].get_attribute('innerHTML')
                        file_link = entries[2].find_element_by_css_selector('a').get_attribute('href')

                        act_link = 'https://map1.msc.fema.gov/data' + file_link[file_link.find('filepath') + 9 : file_link.find('.pdf') + 4]
                        # print(file_id, file_date, file_link)

                        # Download and write to csv
                        if int(file_date[-4:]) >= 2000:
                            urlretrieve(act_link, outp_path + '/' + file_id + '.pdf')
                            outp.writerow([file_id, file_date])

                    try:
                        # Click next to go to next page
                        next_button = his_loma_root_elt.find_element_by_css_selector('.next:not(.disabled)')
                        next_button.click()
                        _ = WebDriverWait(driver, 120).until(
                            lambda dr: his_loma_root_elt.find_element_by_class_name('dataTables_info').get_attribute('innerHTML') != prev_header
                        )
                        prev_header = his_loma_root_elt.find_element_by_class_name('dataTables_info').get_attribute('innerHTML')
                        print(prev_header)

                    except NoSuchElementException as e:
                        break

finally:
    driver.quit()
