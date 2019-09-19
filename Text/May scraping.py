from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(2)
driver.get("https://www.gov.uk/search/news-and-communications?keywords=speech&people%5B%5D=theresa-may&order=updated-newest")


dateDiv = "app-c-published-dates " #class
titleDiv = "gem-c-title__text--long"#class
nextDiv = "gem-c-pagination__item--next" #a
contextDiv = "gem-c-title__context"#p used to check if speech
contentDiv = "govspeak" #div


txt = open("./May speeches/links.txt", 'w')
links = []
firstElement = None
passed = 0

def getLinks():
    elements = driver.find_elements_by_class_name("gem-c-document-list__item  ")
    firstElement = elements[0]
    for x in elements:
        link = x.find_element_by_tag_name('a')
        links.append(link.get_attribute("href"))
        print(link.get_attribute("href"))
    return firstElement
try:
    while True:
        driver.implicitly_wait(2)
        firstElement = getLinks()
        driver.implicitly_wait(5)
        driver.get(driver.find_element_by_class_name(nextDiv).find_element_by_tag_name('a').get_attribute("href"))
        driver.implicitly_wait(5)
except Exception as e:
    print('not found')
    traceback.print_exc()
    pass

for i,x in enumerate(links):
    driver.get(x)
    if driver.find_element_by_class_name(contextDiv).text == "News story" or driver.find_element_by_class_name(contextDiv).text == "Press release":
        continue
    txt.write(x+"\n")
    speech = open(f'./May speeches/Speech{len(links)-i}','w', encoding="utf-8")
    date = " ".join(driver.find_element_by_class_name(dateDiv).text.split(" ")[1:])

    title = driver.find_element_by_class_name(titleDiv).text
    speech.write(f"{'Theresa May'}|{title}|{date}")
    content = driver.find_element_by_class_name(contentDiv).find_elements_by_tag_name('p')
    for t in content:
        speech.write("\n")
        speech.write(t.text)
    speech.close()
txt.close()
