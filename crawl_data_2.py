import csv, time, keyboard
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

latest_end = 0
with open('Done_Index.txt', 'r') as g:
    latest_end = int(list(g)[-1])

with open('Movie_Link.txt', 'r') as f:
    links = [i.strip() for i in list(f)]

with open('error_pos.txt', 'r') as f:
    error_pos = [int(i.strip()) for i in list(f)]

def toMinutes(text):
    ht, mt = text.split('h')
    h, m = 0, 0
    for i in ht:
        if i.isdigit():
            h = h*10 + int(i)
    for i in mt:
        if i.isdigit():
            m = m*10 + int(i)
    return h*60+m

def toInt(text):
    num = 0
    div = 1
    d = False
    for i in text:
        if i.isdigit():
            num = num*10 + int(i)
            if d:
                div *= 10
        elif i == 'K':
            num *= 1000
        elif i == 'M':
            num *= 1000000
        elif i == '.':
            d = True
    return int(num / div)

def getYear(text):
    return toInt(text.split(',')[1])

columns = ['Name', 'Release Year', 'Certificate', 'Duration', 'Poster', 'Trailer', 'Genre', 'Rating', 'Rating Count', 'Country', 'Director', 'Writer', 'Stars', 'Storyline', 'Cost', 'Income']

driver = webdriver.Firefox()
with open('Movie_Data.csv', 'a', newline='\n', encoding="utf-8") as f:
    w = csv.DictWriter(f, columns)
    # w.writeheader()
    with open('Done_Index.txt', 'a') as g:
        for index, link in enumerate(links):
            if index <= latest_end:
                continue

            if keyboard.is_pressed('q'):
                print(index)
                break

            internet_access = False
            while not internet_access and not keyboard.is_pressed('w'):
                try:
                    driver.get(link)
                    internet_access = True
                except:
                    time.sleep(10)
            time.sleep(3)

            data = {}

            try:
                title = driver.find_element(By.XPATH, '//div[@class="sc-e226b0e3-3 dwkouE"]')
                data['Name'] = title.find_element(By.XPATH, './/span[@class="sc-7f1a92f5-1 benbRT"]').get_attribute("textContent")
                present = title.find_elements(By.XPATH, './/li[@class="ipc-inline-list__item"]')
                # data['Release Year'] = present[0].get_attribute("textContent")
                data['Certificate'] = present[1].get_attribute("textContent")
                data['Duration'] = toMinutes(present[-1].get_attribute("textContent"))
            except Exception as error:
                print(f'Title error at {index}')
                print(error)
                print()
                pass

            try:
                intro = driver.find_element(By.XPATH, '//div[@class="sc-e226b0e3-5 kIBBK"]')
                data['Poster'] = intro.find_element(By.XPATH, './/img[@class="ipc-image"]').get_attribute('src')
                after_trailer = driver.find_element(By.XPATH, './/a[@data-testid="video-player-slate-overlay"]').get_attribute('href')
            except Exception as error:
                try:
                    intro = driver.find_element(By.XPATH, '//div[@class="sc-e226b0e3-5 ckgIjw"]')
                    data['Poster'] = intro.find_element(By.XPATH, './/img[@class="ipc-image"]').get_attribute('src')
                    after_trailer = None
                except Exception as error2:
                    print(f'Intro error at {index} type 1')
                    print(error)
                    print(f'Intro error at {index} type 2')
                    print(error2)
                print()
                pass

            try:
                infor = driver.find_element(By.XPATH, '//div[@class="sc-e226b0e3-6 CUzkx"]')
                data['Genre'] = str([a.get_attribute("textContent") for a in infor.find_elements(By.XPATH, './/a[@class="ipc-chip ipc-chip--on-baseAlt"]')])[1:-1].replace("'", "")
                data['Rating'] = float(infor.find_element(By.XPATH, '//span[@class="sc-bde20123-1 cMEQkK"]').get_attribute("textContent"))
                data['Rating Count'] = toInt(infor.find_element(By.XPATH, '//div[@class="sc-bde20123-3 gPVQxL"]').get_attribute("textContent"))
            except Exception as error:
                try:
                    infor = driver.find_element(By.XPATH, '//div[@class="sc-e226b0e3-6 aQqbp"]')
                    data['Genre'] = str([a.get_attribute("textContent") for a in infor.find_elements(By.XPATH, './/a[@class="ipc-chip ipc-chip--on-baseAlt"]')])[1:-1].replace("'", "")
                    data['Rating'] = float(infor.find_element(By.XPATH, '//span[@class="sc-bde20123-1 cMEQkK"]').get_attribute("textContent"))
                    data['Rating Count'] = toInt(infor.find_element(By.XPATH, '//div[@class="sc-bde20123-3 gPVQxL"]').get_attribute("textContent"))
                except Exception as error2:
                    print(f'Infor error at {index} type 1')
                    print(error)
                    print(f'Infor error at {index} type 2')
                    print(error2)
                print()
                pass

            try:
                detail = driver.find_element(By.XPATH, '//section[@data-testid="Details"]')
                data['Country'] = detail.find_element(By.XPATH, './/li[@data-testid="title-details-origin"]').find_element(By.XPATH, './/a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]').get_attribute("textContent")
                data['Release Year'] = detail.find_element(By.XPATH, './/li[@data-testid="title-details-releasedate"]').find_element(By.XPATH, './/a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]').get_attribute("textContent")
                data['Release Year'] = getYear(data['Release Year'])
            except Exception as error:
                print(f'Detail error at {index}')
                print(error)
                print()
                pass

            try:
                title_cast = driver.find_element(By.XPATH, '//section[@data-testid="title-cast"]')
                data['Director'] = title_cast.find_element(By.XPATH, './/a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]').get_attribute("textContent")
                data['Writer'] = str([a.get_attribute("textContent") for a in title_cast.find_elements(By.XPATH, './/a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')[1:]])[1:-1].replace("'", "")
                data['Stars'] = str([a.get_attribute("textContent") for a in title_cast.find_elements(By.XPATH, './/a[@data-testid="title-cast-item__actor"]')])[1:-1].replace("'", "")
            except Exception as error:
                print(f'Title cast error at {index}')
                print(error)
                print()
                pass

            try:
                box_office = driver.find_element(By.XPATH, '//section[@data-testid="BoxOffice"]')
                data['Income'] = toInt(box_office.find_element(By.XPATH, './/li[@data-testid="title-boxoffice-cumulativeworldwidegross"]').find_element(By.XPATH, './/span[@class="ipc-metadata-list-item__list-content-item"]').get_attribute("textContent"))
                data['Cost'] = toInt(box_office.find_element(By.XPATH, '//li[@data-testid="title-boxoffice-budget"]').find_element(By.XPATH, './/span[@class="ipc-metadata-list-item__list-content-item"]').get_attribute("textContent"))
            except Exception as error:
                print(f'Box office error at {index}')
                print(error)
                print()
                pass
            
            try:
                storyline = driver.find_element(By.XPATH, '//p[@class="sc-466bb6c-3 fOUpWp"]')
                data['Storyline'] = storyline.find_element(By.XPATH, './/span[@class="sc-466bb6c-1 dWufeH"][@data-testid="plot-l"]').get_attribute("textContent")
            except Exception as error:
                try:
                    storyline = driver.find_element(By.XPATH, '//div[@class="sc-e226b0e3-6 aQqbp"]')
                    data['Storyline'] = storyline.find_element(By.XPATH, './/span[@class="sc-466bb6c-0 hlbAws"][@data-testid="plot-xs_to_m"]').get_attribute("textContent")
                except Exception as error2:
                    print(f'Storyline error at {index} type 1')
                    print(error)
                    print(f'Storyline error at {index} type 2')
                    print(error2)
                print()
                pass

            try:
                if after_trailer == None:
                    continue
                driver.get(after_trailer)
                time.sleep(3)
                data['Trailer'] = driver.find_element(By.XPATH, '//video[@class="jw-video jw-reset"]').get_attribute('src')
            except Exception as error:
                print(f'Get link Trailer error at {index}')
                print(error)
                print()
                pass

            w.writerow(data)
            g.write(f'{index}\n')
driver.close()