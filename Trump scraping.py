from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import datetime

def clickable(element):
    clicked = 0
    while clicked < 10:
        try:
            print(f'clicked {clicked} times')
            time.sleep(.5)
            clicked+=1
            element.click()
            return True
        except selenium.common.exceptions.ElementNotInteractableException :
            pass
    return False

def enterDate(date):
    m,d,y = date.month,date.day,date.year
    driver.execute_script("document.getElementsByClassName('daterangepicker')[1].style.display = 'block';")
    for inp in datepicker.find_elements_by_class_name('input-mini'):
        inp.send_keys(Keys.CONTROL + "a")
        inp.send_keys(Keys.DELETE)
        inp.send_keys(f"{m:02d}/{d:02d}/{y}\n")
    print(f"{m:2d}/{d:2d}/{y}\n")
    active = datepicker.find_element_by_class_name('start-date')
    active.click()
    active = datepicker.find_element_by_class_name('start-date')
    active.click()
    active = datepicker.find_element_by_class_name('start-date')
    active.click()
    driver.implicitly_wait(5)

driver = webdriver.Chrome("./chromedriver")
driver.set_window_size(1080, 768)
driver.get("https://factba.se/search#speech")
driver.implicitly_wait(5)
datepicker = driver.find_elements_by_class_name('daterangepicker')[1]

driver.execute_script("document.getElementsByClassName('daterangepicker')[1].style.display = 'block';")
datepicker.find_elements_by_tag_name('li')[-1].click()

headerDiv = "transcript-header" #class
contentDiv = "resultsblock" #id
d = datetime.datetime(2016, 6, 1)
links = open("./Trump speeches/links.txt", 'r').readlines()

txt = open("./Trump speeches/links.txt", 'a')
failed = open("./Trump speeches/failed.txt", 'a')
firstElement = None
passed = 0
def getLinks():
    elements = driver.find_element_by_class_name("infinite").find_elements_by_tag_name('small')
    if len(elements) == 0:
        return
    for x in elements:
        l = x.find_element_by_tag_name('a').get_attribute('href')
        if "youtube" in l:
            continue
        if l not in links:
            links.append(l)
            print(l)
            txt.write(l+"\n")
    return elements[0]

'''
while d < datetime.datetime.now():
    enterDate(d)
    getLinks()
    d += datetime.timedelta(days=1)
txt.close()'''


for i,x in enumerate(links):
    try:
        driver.get(x)
        speech = open(f'./Trump speeches/Speech{len(links)-i}','w', encoding="utf-8")
        header = driver.find_element_by_class_name(headerDiv).text.split("-")
        date = header[1].strip()
        title = header[0].strip()
        speech.write(f"{'Donald Trump'}|{title}|{date}")
        content = driver.find_element_by_id(contentDiv).find_elements_by_xpath('*')
        print(x)
        for t in range(1,len(content)//2):
            speech.write("\n")
            speech.write(driver.find_element_by_name(f'seq{t}').text)
        speech.close()
    except Exception as e:
        traceback.print_exc()
        failed.write(x)
txt.close()
failed.close()
