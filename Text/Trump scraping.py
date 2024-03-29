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
import pickle

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

txt = open("./Trump speeches/passed.txt", 'w')
#failed links are stored for later recovery if needed
failed = open("./Trump speeches/failed.txt", 'w')
firstElement = None
passed = 0
def getLinks(date):
    m,d,y = date.month,date.day,date.year
    elements = driver.find_element_by_class_name("infinite").find_elements_by_tag_name('small')
    if len(elements) == 0:
        return
    for x in elements:
        l = x.find_element_by_tag_name('a').get_attribute('href')
        if "youtube" in l:
            continue
        if ("{m:2d}/{d:2d}/{y}\n",l) not in links:
            links.append(("{m:2d}/{d:2d}/{y}\n",l))
            print(l)
    return elements[0]
    
# go through each date and get links, as page scrolls infinitely, it is easier to ensure complete coverage by going through dates one by one
try:
    with open('trump links.pkl', 'rb') as f:
        links = pickle.load(f)
except:
    print("couldn't load saves, restarting")
    links = []
    while d < datetime.datetime.now():
        enterDate(d)
        getLinks(d)
        d += datetime.timedelta(days=1)
    with open('trump links.pkl', 'wb') as f:
        pickle.dump(links, f)
    

for i,tup in enumerate(links):
    date,x = tup
    try:
        driver.get(x)
        header = driver.find_element_by_class_name(headerDiv).text.split("-")
        date = header[1].strip()
        title = header[0].strip()
        speech = open(f'./Trump speeches/Speech{i}','w', encoding="utf-8")
        speech.write(f"{'Donald Trump'}|{title}|{date}")
        Type = title.split(":")[0]
        print(Type)
        content = driver.find_element_by_id(contentDiv).find_elements_by_xpath('*')
        #if not speech, check if speaker is trump, else grab all relevant text
        if Type != "Speech":
            header = driver.find_element_by_class_name("transcript-header").text.split("-")
            date = header[1].strip()
            title = header[0].strip()
            elements = driver.find_element_by_id('resultsblock').find_elements_by_xpath("*")
            adjust = 0
            for j in range(1,len(content)//2):
                try:
                    #sometimes speech blocks skip number, need to check if scraping is actually complete
                    e = driver.find_element_by_name(f'seq{j+adjust}').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
                    if e.find_element_by_class_name('speaker-label').text == "Donald Trump":
                        speech.write("\n")
                        speech.write(driver.find_element_by_name(f'seq{j}').text)
                except:
                    try:
                        adjust+=1
                        e = driver.find_element_by_name(f'seq{j+adjust}').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
                        if e.find_element_by_class_name('speaker-label').text == "Donald Trump":
                            speech.write("\n")
                            speech.write(driver.find_element_by_name(f'seq{j}').text)
                    except:
                        traceback.print_exc()
                        failed.write(x)
                        continue
            txt.write(x)
        else:
            try:
                adjust = 0
                for t in range(1,len(content)//2):
                    speech.write("\n")
                    speech.write(driver.find_element_by_name(f'seq{t+adjust}').text)
                txt.write(x)
            except:
                adjust += 1
                speech.write("\n")
                speech.write(driver.find_element_by_name(f'seq{t+adjust}').text)
                continue
        speech.close()
    except Exception as e:
        traceback.print_exc()
        failed.write(x)
txt.close()
failed.close()
