from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import setting as S
import traceback
import time


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
	url_list = []
	driver.get('https://kenkoooo.com/atcoder/#/contest/recent')
	wait.until(EC.presence_of_all_elements_located)
	time.sleep(1)
	display_All()
	table =  driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div/div/div[2]/div[2]/table/tbody')
	trs = table.find_elements(by = By.TAG_NAME, value = 'tr')
	for tr in trs:
		tds = tr.find_elements(by = By.TAG_NAME, value = 'td')
		date = tds[3].find_element(by = By.TAG_NAME, value = 'div').get_attribute("textContent")
		date = date.split(' ')[0]
		print(date)
		title = tds[0].find_element(by = By.TAG_NAME, value = 'a').get_attribute("textContent")
		href = tds[0].find_element(by = By.TAG_NAME, value = 'a').get_attribute("href")
		title = title[7:]
		print(title)
		if title == contest_title:
			url_list.append((href, date))
	return url_list

def collect_past_log(url, date):
	driver.get(url)
	wait.until(EC.presence_of_all_elements_located)
	time.sleep(1)
	file = open(S.Dir_path + '/log/' + date, 'w')
	table_2 = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div[2]/div/table/tbody')
	tr_2 = table_2.find_elements(by = By.TAG_NAME, value = 'tr')
	for problem in tr_2:
		tds_2 = problem.find_elements(by = By.TAG_NAME, value = 'td')
		problem_url = tds_2[0].find_element(by = By.TAG_NAME, value = 'a').get_attribute('href')
		problem_name = problem_url.split('/')[-1]
		file.write(problem_name + '\n')
	file.close()

def main():
	try:
		url_list = collect_contests_url()
		print("")
		for (url, date) in url_list:
			print("logに追加中 (" + date + ")")
			collect_past_log(url, date)
	except Exception:
		print(traceback.format_exc())
	finally:
		driver.close()


if __name__ == '__main__':
	chrome_service = service.Service(executable_path = S.chromedriver_path)
	chrome_options = Options()
	if not display_browser:
		chrome_options.add_argument('-headless')
	driver = webdriver.Chrome(service = chrome_service, options = chrome_options)
	wait = WebDriverWait(driver = driver, timeout = 60)
	main()
