from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from os import listdir
print(listdir())
driver = webdriver.Chrome("./chromedriver")
driver.get("https://www.pm.gov.au/media")
driver.implicitly_wait(5)
select = Select(driver.find_element_by_id('edit-field-media-type-value'))
select.select_by_value('speech')
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 5)
driver.find_element_by_id("edit-submit-media-centre-page").click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "throbber")))
WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, "throbber")))


dateDiv = "media-date" #class
titleDiv = "pagetitle"#class
txt = open("./Scomo speeches/links.txt", 'w')
links = []
firstElement = None

def getLinks():
    elements = driver.find_elements_by_class_name("media-item")
    firstElement = elements[0]
    for x in elements:
        link = x.find_element_by_tag_name('a')
        links.append(link.get_attribute("href"))
    return firstElement

#get links
try:
    while True:
        driver.implicitly_wait(2)
        firstElement = getLinks()
        driver.implicitly_wait(2)
        driver.get(driver.find_element_by_class_name('pager-next').find_element_by_tag_name('a').get_attribute("href"))
        driver.implicitly_wait(2)
except Exception as e:
    print('not found')
    traceback.print_exc()
    pass
#scrape text from each link
for i,x in enumerate(links):
    driver.get(x)
    txt.write(x+"\n")
    speech = open(f'./Scomo speeches/Speech{len(links)-i}','w', encoding="utf-8")
    date = driver.find_element_by_class_name(dateDiv)
    while date.text == "":
        time.sleep(.5)
    title = driver.title.split("|")[0].strip()
    speech.write(f"{'Scott Morrison'}|{title}|{date.text}")
    print(date.text)
    content = driver.find_elements_by_class_name('even')
    speech.write("\n")
    speech.write(content[2].text.strip())
