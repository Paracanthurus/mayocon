from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import setting as S
import traceback
import time
import datetime
import subprocess


contest_title = S.Contest_Title

display_browser = False

def display_All():
	dropdown = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div/div/div[1]/div/div[1]/span')
	bottun = dropdown.find_element(by = By.TAG_NAME, value = 'button')
	driver.execute_script("arguments[0].click();", bottun)
	time.sleep(1)
	ul = dropdown.find_element(by = By.TAG_NAME, value = 'ul')
	li = ul.find_elements(by = By.TAG_NAME, value = 'li')
	li[4].find_element(by = By.TAG_NAME, value = 'a').click()
	wait.until(EC.presence_of_all_elements_located)
	time.sleep(1)

def collect_contests_url():
	driver.get('https://kenkoooo.com/atcoder/#/contest/recent')
	wait.until(EC.presence_of_all_elements_located)
	time.sleep(1)
	display_All()
	table =  driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div/div/div[2]/div[2]/table/tbody')
	trs = table.find_elements(by = By.TAG_NAME, value = 'tr')
	for tr in trs:
		tds = tr.find_elements(by = By.TAG_NAME, value = 'td')
		date = tds[4].find_element(by = By.TAG_NAME, value = 'div').get_attribute("textContent")
		date = date.split(' ')[0]
		title = tds[0].find_element(by = By.TAG_NAME, value = 'a').get_attribute("textContent")
		href = tds[0].find_element(by = By.TAG_NAME, value = 'a').get_attribute("href")
		title = title[7:]
		if date < str(datetime.datetime.today().date()):
			return 'no_contest'
		if title == S.Contest_Title:
			return href

def collect_ranking(url):
	driver.get(url)
	wait.until(EC.presence_of_all_elements_located)
	time.sleep(1)
	table = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div[2]/div/table')
	tbody = table.find_element(by = By.TAG_NAME, value = 'tbody')
	users = tbody.find_elements(by = By.TAG_NAME, value = 'tr')
	users.pop(-1)
	names = '\`\`\`'
	c = 1
	for user in users:
		name = user.find_element(by = By.TAG_NAME, value = 'a').text
		names += '{:>2d}: {}'.format(c, name) + '\n'
		c += 1
	names += '\`\`\`'
	return names

def main(Driver, Wait):
	try:
		global driver
		global wait
		driver = Driver
		wait = Wait
		url = collect_contests_url()
		if url == 'no_contest':
			return
		url += '?activeTab=Standings'
		w_list = ['月', '火', '水', '木', '金', '土', '日']
		Today = datetime.datetime.today().date()
		bot_msg = '%d月%d日(%s)の結果発表!\n'%(Today.month, Today.day, w_list[Today.weekday()])
		bot_msg += collect_ranking(url)
	except Exception:
		print(traceback.format_exc())
		bot_msg = 'err'
	finally:
		if S.discordbot and not S.bot_off:
			subprocess.call('python3 ' + S.Dir_path + '/discordbot.py "' + bot_msg + '" "' + str(S.result_channel_id) + '"', shell = True)


if __name__ == '__main__':
	chrome_service = service.Service(executable_path = S.chromedriver_path)
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	if not S.Display_Browser:
		chrome_options.add_argument('--headless')
	driver = webdriver.Chrome(service = chrome_service, options = chrome_options)
	wait = WebDriverWait(driver = driver, timeout = 60)
	main()
	driver.quit()
