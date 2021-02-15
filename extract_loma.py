import mechanicalsoup as ms
from bs4 import BeautifulSoup
import urllib

browser = ms.StatefulBrowser()
browser.open('https://msc.fema.gov/portal/advanceSearch')

form = browser.select_form('form[id=catalogSearchForm]')
form['selstate'] = '12'

# print(form['selcounty'])
# browser.launch_browser()

search_btn = browser.page.find_all(id='mainSearch')[0]
print(search_btn, type(search_btn))
print(form.print_summary())
form.choose_submit(search_btn)
browser.submit_selected()

print(form.print_summary())