import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from time import sleep

from bs4 import BeautifulSoup

from pychord import Chord

url = str(input('chordify 링크를 입력하세요.: '))
capo_fret_loc = int(input("카포 위치가 몇 번째 프렛입니까?: "))



## 이걸 제대로 만들어야 된다.
def set_guitar_code(ori_key, capo_fret=capo_fret_loc):
    ok = ori_key.split('_')
    baseChord = ok[0].replace('s', '#')
    etcChord = ''.join(ok[1:])

    c = Chord(baseChord)
    c.transpose(-capo_fret)

    # print(str(c) + '_' + etcChord)

    return (str(c).replace('#', 's') + '_' + etcChord)



chromedriver_autoinstaller.install('./')

driver = webdriver.Chrome()

driver.get(url)
sleep(3)

try:
    driver.find_element_by_xpath('//*[@id="chordsArea"]/div[3]/div[1]/header').click()
except exceptions.NoSuchElementException:
    pass

sleep(3)

try:
    driver.find_element_by_xpath('//*[@id="song"]/div[2]/div/div[3]/div[3]/div[2]/div/div/button').click()
except exceptions.NoSuchElementException:
    pass

sleep(1)


ori_chords = driver.find_element_by_css_selector('#edit-toolbar-legacy > li:nth-child(1) > span > a > span > span')
ori_trans = ori_chords.get_attribute('class').split('label-')[1]
changed_trans = set_guitar_code(ori_trans)
driver.execute_script(f'arguments[0].setAttribute("class", "label-{changed_trans}")', ori_chords)





s = BeautifulSoup(driver.page_source, 'html.parser')
chords_len = len(s.find('div', {'id':'chords'}).find_all('div', {'class':'label-wrapper'}))


for i in range(chords_len):
    try:
        ori = driver.find_element_by_xpath(f'//*[@id="chords"]/div[{i+1}]/div/span[1]')
        oriChord = ori.get_attribute('class').split('chord-label label-')[1]
        changedChord = set_guitar_code(ori_key=oriChord)

        driver.execute_script(f'arguments[0].setAttribute("class", "chord-label label-{changedChord}")', ori)
    except IndexError:
        pass



chords_len2 = len(s.find('div', {'id':'diagrams'}).find_all('img'))

for i in range(chords_len2):
    try:
        img = driver.find_element_by_xpath(f'//*[@id="diagrams"]/div[{i}]/img')
        chord = driver.find_element_by_xpath(f'//*[@id="diagrams"]/div[{i}]/div/div/span')

        changedChord = set_guitar_code(ori_key=str(chord.get_attribute('class')).split('label-')[1])
        
        driver.execute_script(f'arguments[0].setAttribute("src", "//chordify.net/img/diagrams/guitar/{changedChord}.png?1")', img)
        driver.execute_script(f'arguments[0].setAttribute("class", "label-{changedChord}")', chord)

    except IndexError:
        pass

    except exceptions.NoSuchElementException:
        pass