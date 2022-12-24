from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import setting as S
import resultbot
import sys
import datetime
import re
import os
import traceback
import subprocess
import time


login_url = 'https://github.com/login?client_id=162a5276634fc8b970f7&return_to=%2Flogin%2Foauth%2Fauthorize%3Fclient_id%3D162a5276634fc8b970f7%26redirect_uri%3Dhttps%253A%252F%252Fkenkoooo.com%252Fatcoder%252Finternal-api%252Fauthorize%253Fredirect_to%253D%25252F'
contest_url = 'https://kenkoooo.com/atcoder/#/contest/create'
atcoder_url = 'https://atcoder.jp/contests/'

bot_msg = ''


class Time:

	def __init__(self):

		Start_date = datetime.datetime.today() + datetime.timedelta(days = S.Start_Day)

		Start_time = re.findall('[0-9]+', S.Start_Time)
		if (len(Start_time) != 2):
			sys.exit("Start_Time は '21:00' や '21-00' のような形式で入力してください")

		Start_hour = int(Start_time[0])
		if Start_hour < 0 or 24 <= Start_hour:
			sys.exit('Start_Time が無効です')

		Start_minute = int(Start_time[1])
		if Start_minute < 0 or 60 <= Start_minute:
			sys.exit('Start_Time が無効です')
		if Start_minute % 5 != 0:
			sys.exit('Start_Time は 5分刻みで入力してください')

		self.Start = datetime.datetime(year = Start_date.year, month = Start_date.month, day = Start_date.day, hour = Start_hour, minute = Start_minute)
		if self.Start < datetime.datetime.now():
			sys.exit('Start_Time が早すぎます')

		delta_time = 0
		if type(S.Duration) is str:
			Duration = re.findall('[0-9]+', S.Duration)
			if (len(Duration) != 1 and len(Duration) != 2):
				sys.exit("Duration は '1:40' あるいは 100 の形式で入力してください")
			delta_time += int(Duration[-1])
			if len(Duration) == 2:
				delta_time += int(Duration[0]) * 60
		elif type(S.Duration) is int:
			delta_time += S.Duration
		else:
			sys.exit('Duration が無効です')
		if delta_time % 5 != 0:
			sys.exit('Duration は 5分刻みで入力してください')

		self.End_time = self.Start + datetime.timedelta(minutes = delta_time)


def del_oldlog():
	del_date = (datetime.datetime.now() - datetime.timedelta(days = S.Del_logfile_span)).date()
	files = os.listdir(S.Dir_path + '/log/')
	for file in files:
		if file < str(del_date) + '.log' and file != '.gitkeep':
			os.remove(S.Dir_path + '/log/' + file)


def insert_set(st):
	start_date = T.Start.date()
	for n in range(S.Exclude_past_days + 1):
		date = start_date - datetime.timedelta(days = n)
		if os.path.exists(S.Dir_path + '/log/' + str(date) + '.log'):
			logfile = open(S.Dir_path + '/log/' + str(date) + '.log', 'r')
			problem_list = logfile.readlines()
			for problem in problem_list:
				st.add(problem.strip('\n'))
			logfile.close()
		else:
			continue


def contest_exists():
	driver.get(atcoder_url)
	wait.until(EC.presence_of_all_elements_located)
	global bot_msg
	w_list = ['月', '火', '水', '木', '金', '土', '日']
	table =  driver.find_element(by = By.ID, value = 'contest-table-upcoming')
	table_body = table.find_element(by = By.TAG_NAME, value = 'tbody')
	contests = table_body.find_elements(by = By.TAG_NAME, value = 'tr')
	for contst in contests:
		tds = contst.find_elements(by = By.TAG_NAME, value = 'td')
		if str(T.Start.date()) in tds[0].text:
			href = tds[1].find_element(by = By.TAG_NAME, value = 'a').get_attribute('href')
			if S.No_contest_day_ABC and 'abc' in href:
				bot_msg = '%d月%d日(%s)はABC!\n'%(T.Start.month, T.Start.day, w_list[T.Start.weekday()]) + href
				return 1
			if S.No_contest_day_ARC and 'arc' in href:
				bot_msg = ('%d月%d日(%s)はARC!\n'%(T.Start.month, T.Start.day, w_list[T.Start.weekday()])) + href
				return 1
			if S.No_contest_day_AGC and 'agc' in href:
				bot_msg = ('%d月%d日(%s)はAGC!\n'%(T.Start.month, T.Start.day, w_list[T.Start.weekday()])) + href
				return 1
	return 0


def login():
	driver.get(login_url)
	wait.until(EC.presence_of_all_elements_located)
	driver.find_element(by = By.ID, value = 'login_field').send_keys(S.username_github)
	driver.find_element(by = By.ID, value = 'password').send_keys(S.password_github)
	driver.find_element(by = By.ID, value = 'password').send_keys(Keys.RETURN)
	wait.until(EC.presence_of_all_elements_located)
	time.sleep(60)
	wait.until(EC.presence_of_all_elements_located)
	if driver.current_url == 'https://github.com/sessions/verified-device':
		if S.Display_Browser:
			print('2段階認証が必要です')
			for t in range(300):
				time.sleep(1)
				if driver.current_url == 'https://kenkoooo.com/atcoder/#/table/':
					break
		if driver.current_url != 'https://kenkoooo.com/atcoder/#/table/':
			sys.exit('2段階認証が必要です')
	elif driver.current_url != 'https://kenkoooo.com/atcoder/#/table/':
		time.sleep(5)
		authorize_button = driver.find_element(by = By.ID, value = 'js-oauth-authorize-btn')
		driver.execute_script("arguments[0].click();", authorize_button)
		wait.until(EC.presence_of_all_elements_located)
		time.sleep(3)
		wait.until(EC.presence_of_all_elements_located)


def create_contest():
	recently_set = set()
	insert_set(recently_set)
	back_space = ''
	for i in range(4):
		back_space += Keys.BACK_SPACE
	driver.get(contest_url)
	wait.until(EC.presence_of_all_elements_located)
	if driver.current_url == 'https://kenkoooo.com/atcoder/#/table/':
		sys.exit('ログインしていません')
	time.sleep(3)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[2]/div/input').send_keys(S.Contest_Title)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[3]/div/textarea').send_keys(S.Description)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[4]/div/div/div/button').click()
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[4]/div/div/div/div/button[' + str(S.Public_State) + ']').click()
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[5]/div/div/div/button').click()
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[5]/div/div/div/div/button[' + str(S.Mode) + ']').click()
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div/input').send_keys(back_space + str(S.Penalty))
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[7]/div/div/input').send_keys(str(T.Start.year).zfill(6) + str(T.Start.month).zfill(2) + str(T.Start.day).zfill(2))
	Select(driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[7]/div/div/select[1]')).select_by_index(T.Start.hour)
	Select(driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[7]/div/div/select[2]')).select_by_index(int(T.Start.minute / 5))
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[8]/div/div/input').send_keys(str(T.End_time.year).zfill(6) + str(T.End_time.month).zfill(2) + str(T.End_time.day).zfill(2))
	Select(driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[8]/div/div/select[1]')).select_by_index(T.End_time.hour)
	Select(driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[8]/div/div/select[2]')).select_by_index(int(T.End_time.minute / 5))
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[9]/div/input').send_keys(S.Expected_Participants)
	checkbox = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[1]/div/div/div/span/input')
	if S.Exclude_experimental_difficulty != checkbox.is_selected():
		driver.execute_script("arguments[0].click();", checkbox)
		wait.until(EC.presence_of_all_elements_located)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[2]/div/div/div/button').click()
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[2]/div/div/div/div/button[' + str(S.Exclude_probrems) + ']').click()
	for i in range(5):
		driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[4]/div/button').click()
		wait.until(EC.presence_of_all_elements_located)
	if not S.No_log:
		logfile = open(S.Dir_path + '/log/' + str(T.Start.date()) + '.log', 'a')
	end_time = datetime.datetime.now() + datetime.timedelta(seconds = S.Timelimit_Find_problems)
	for n in range(len(S.Problems)):
		if datetime.datetime.now() > end_time:
			if not S.No_log:
				logfile.close()
			sys.exit('問題の制限が厳しすぎます')
		driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[4]/div/div/input[1]').send_keys(back_space + str(S.Problems[n][0]))
		driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[4]/div/div/input[2]').send_keys(back_space + str(S.Problems[n][1]))
		while True:
			driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[6]/div[1]/button').click()
			time.sleep(0.5)
			wait.until(EC.presence_of_all_elements_located)
			problem_id = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[10]/div/div/div/table/tbody/tr[' + str(n + 1) + ']').get_attribute('data-rbd-draggable-id')
			if 'abc' in problem_id or not S.ABC_Only:
				if not problem_id in recently_set:
					if not S.No_log:
						logfile.write(problem_id + '\n')
					break
			del_button = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[10]/div/div/div/table/tbody/tr[' + str(n + 1) + ']/td[5]/button')
			driver.execute_script("arguments[0].click();", del_button)
			time.sleep(0.5)
			wait.until(EC.presence_of_all_elements_located)
	if not S.No_log:
		logfile.close()
	if S.Sort_Difficulty:
		diff_sort = driver.find_element(by = By.CSS_SELECTOR, value = '#root > div > div.my-5.container > div:nth-child(12) > div > div > div > table > thead > tr > th:nth-child(3)')
		driver.execute_script("arguments[0].click();", diff_sort)
		time.sleep(1)
		wait.until(EC.presence_of_all_elements_located)
	for n in range(len(S.Problems)):
		point = driver.find_element(by = By.CSS_SELECTOR, value = '#root > div > div.my-5.container > div:nth-child(12) > div > div > div > table > tbody > tr:nth-child(' + str(n + 1) + ') > td:nth-child(4)')
		driver.execute_script("arguments[0].click();", point)
		if n < len(S.Points):
			point.find_element(by = By.TAG_NAME, value = 'input').send_keys(str(S.Points[n]))
		point.find_element(by = By.TAG_NAME, value = 'input').send_keys(Keys.ENTER)
		time.sleep(0.5)
	if not S.No_create_contest:
		create_button = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[13]/div/button')
		driver.execute_script("arguments[0].click();", create_button)
		wait.until(EC.presence_of_all_elements_located)
		time.sleep(60)
		wait.until(EC.presence_of_all_elements_located)
		if driver.current_url == contest_url:
			sys.exit('コンテストの作成に失敗しました')
	global bot_msg
	w_list = ['月', '火', '水', '木', '金', '土', '日']
	bot_msg = '%d月%d日(%s) %s開催!\n'%(T.Start.month, T.Start.day, w_list[T.Start.weekday()], S.Contest_Title) + driver.current_url


def main():
	global T
	T = Time()
	del_oldlog()
	if not contest_exists():
		login()
		create_contest()


if __name__ == '__main__':
	try:
		chrome_service = service.Service(executable_path = S.chromedriver_path)
		chrome_options = Options()
		chrome_options.add_argument('--no-sandbox')
		if not S.Display_Browser:
			chrome_options.add_argument('--headless')
		driver = webdriver.Chrome(service = chrome_service, options = chrome_options)
		wait = WebDriverWait(driver = driver, timeout = 60)
		resultbot.main(driver, wait)
		main()

	except SystemExit as e:
		errlog = open(S.Dir_path + '/err/' + str(datetime.datetime.now().date()) + '.log', 'a')
		errlog.write('\n' + str(datetime.datetime.now()) + '\n')
		errlog.write(str(e) + '\n')
		errlog.close()
		print(str(e))
		bot_msg = 'err'

	except Exception:
		errlog = open(S.Dir_path + '/err/' + str(datetime.datetime.now().date()) + '.log', 'a')
		msg = traceback.format_exc()
		errlog.write('\n' + str(datetime.datetime.now()) + '\n')
		errlog.write(msg + '\n')
		errlog.close()
		print(msg + '\nエラーが発生しました\n')
		bot_msg = 'err'

	finally:
		if S.discordbot and not S.bot_off:
			subprocess.call('python3 ' + S.Dir_path + '/discordbot.py "' + bot_msg + '" "' + str(S.discordbot_channel_id) + '"', shell = True)
		driver.quit()
