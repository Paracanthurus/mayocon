from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
import setting as S
import time
import sys
import datetime
import re
import os
import traceback
import subprocess


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
	files = os.listdir('./log/')
	for file in files:
		if file < str(del_date) and file != '.gitignore':
			os.remove('./log/' + file)


def insert_set(st):
	start_date = T.Start.date()
	for n in range(S.Exclude_past_days + 1):
		date = start_date - datetime.timedelta(days = n)
		if os.path.exists('./log/' + str(date)):
			logfile = open('./log/' + str(date), 'r')
			problem_list = logfile.readlines()
			for problem in problem_list:
				st.add(problem.strip(os.linesep))
			logfile.close()
		else:
			continue


def contest_exists():
	driver.get(atcoder_url)
	time.sleep(5)
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
				bot_msg = '%d月%d日(%s)はABC!'%(T.Start.month, T.Start.day, w_list[T.Start.weekday()])
				return 1
			if S.No_contest_day_ARC and 'arc' in href:
				bot_msg = ('%d月%d日(%s)はARC!'%(T.Start.month, T.Start.day, w_list[T.Start.weekday()]))
				return 1
		time.sleep(0.5)
	return 0


def login():
	driver.get(login_url)
	time.sleep(5)
	driver.find_element(by = By.ID, value = 'login_field').send_keys(S.username_github)
	time.sleep(0.5)
	driver.find_element(by = By.ID, value = 'password').send_keys(S.password_github)
	time.sleep(0.5)
	driver.find_element(by = By.ID, value = 'password').send_keys(Keys.RETURN)
	time.sleep(5)
	if driver.current_url != 'https://kenkoooo.com/atcoder/#/table/':
		sys.exit('ログインに失敗しました')


def create_contest():
	recently_set = set()
	insert_set(recently_set)
	back_space = ''
	for i in range(4):
		back_space += Keys.BACK_SPACE
	driver.get(contest_url)
	time.sleep(5)
	if driver.current_url == 'https://kenkoooo.com/atcoder/#/table/':
		sys.exit('ログインしていません')
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[2]/div/input').send_keys(S.Contest_Title)
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[3]/div/textarea').send_keys(S.Description)
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[4]/div/div/div/button').click()
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[4]/div/div/div/div/button[' + str(S.Public_State) + ']').click()
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[5]/div/div/div/button').click()
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[5]/div/div/div/div/button[' + str(S.Mode) + ']').click()
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div/input').send_keys(back_space + str(S.Penalty))
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[7]/div/div/input').send_keys(str(T.Start.year) + Keys.ARROW_RIGHT + str(T.Start.month) + Keys.ARROW_RIGHT + str(T.Start.day))
	time.sleep(0.5)
	Select(driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[7]/div/div/select[1]')).select_by_index(T.Start.hour)
	time.sleep(0.5)
	Select(driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[7]/div/div/select[2]')).select_by_index(int(T.Start.minute / 5))
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[8]/div/div/input').send_keys(str(T.End_time.year) + Keys.ARROW_RIGHT + str(T.End_time.month) + Keys.ARROW_RIGHT + str(T.End_time.day))
	time.sleep(0.5)
	Select(driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[8]/div/div/select[1]')).select_by_index(T.End_time.hour)
	time.sleep(0.5)
	Select(driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[8]/div/div/select[2]')).select_by_index(int(T.End_time.minute / 5))
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[9]/div/input').send_keys(S.Expected_Participants)
	time.sleep(0.5)
	checkbox = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[1]/div/div/div/span/input')
	if S.Exclude_experimental_difficulty != checkbox.is_selected():
		driver.execute_script("arguments[0].click();", checkbox)
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[2]/div/div/div/button').click()
	time.sleep(0.5)
	driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[2]/div/div/div/div/button[' + str(S.Exclude_probrems) + ']').click()
	time.sleep(0.5)
	for i in range(5):
		driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[4]/div/button').click()
		time.sleep(0.5)
	logfile = open('./log/' + str(T.Start.date()), 'a')
	end_time = datetime.datetime.now() + datetime.timedelta(seconds = S.Timelimit_Find_problems)
	for n in range(len(S.Problems)):
		if datetime.datetime.now() > end_time:
				exit('問題の制限が厳しすぎます')
		driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[4]/div/div/input[1]').send_keys(back_space + str(S.Problems[n][0]))
		time.sleep(0.5)
		driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[4]/div/div/input[2]').send_keys(back_space + str(S.Problems[n][1]))
		time.sleep(0.5)
		while True:
			driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[12]/div/div/div/div/form/div[6]/div[1]/button').click()
			time.sleep(0.5)
			problem_id = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[10]/div/div/div/table/tbody/tr[' + str(n + 1) + ']').get_attribute('data-rbd-draggable-id')
			time.sleep(0.5)
			if 'abc' in problem_id or not S.ABC_Only:
				if not problem_id in recently_set:
					logfile.write(problem_id + os.linesep)
					break
			del_button = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[10]/div/div/div/table/tbody/tr[' + str(n + 1) + ']/td[5]/button')
			driver.execute_script("arguments[0].click();", del_button)
			time.sleep(0.5)
	logfile.close()
	if S.Sort_Difficulty:
		diff_sort = driver.find_element(by = By.CSS_SELECTOR, value = '#root > div > div.my-5.container > div:nth-child(12) > div > div > div > table > thead > tr > th:nth-child(3)')
		driver.execute_script("arguments[0].click();", diff_sort)
		time.sleep(0.5)
	for n in range(len(S.Problems)):
		point = driver.find_element(by = By.CSS_SELECTOR, value = '#root > div > div.my-5.container > div:nth-child(12) > div > div > div > table > tbody > tr:nth-child(' + str(n + 1) + ') > td:nth-child(4)')
		driver.execute_script("arguments[0].click();", point)
		time.sleep(0.5)
		if n < len(S.Points):
			point.find_element(by = By.TAG_NAME, value = 'input').send_keys(str(S.Points[n]))
		point.find_element(by = By.TAG_NAME, value = 'input').send_keys(Keys.ENTER)
		time.sleep(0.5)
	if not S.No_create_contest:
		driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[13]/div/button').click()
	time.sleep(5)
	global bot_msg
	bot_msg = S.Contest_Title + '開催!\n' + driver.current_url


def main():
	try:
		del_oldlog()
		global T, driver
		chrome_service = service.Service(executable_path = S.chromedriver_path)
		chrome_options = Options()
		if not S.Display_Browser:
			chrome_options.add_argument('--headless')
		driver = webdriver.Chrome(service = chrome_service, options = chrome_options)
		T = Time()
		if not contest_exists():
			login()
			create_contest()

	except SystemExit as e:
		errlog = open('./err/' + str(datetime.datetime.now()), 'w')
		errlog.write(str(e))
		errlog.close()
		print(str(e))

	except Exception:
		errlog = open('./err/' + str(datetime.datetime.now()), 'w')
		msg = traceback.format_exc()
		errlog.write(msg)
		errlog.close()
		print(msg + '\nエラーが発生しました\n')

	else:
		if S.discordbot and not S.bot_off:
			subprocess.call('python discordbot.py "' + bot_msg + '"', shell = True)

	finally:
		driver.quit()


if __name__ == '__main__':
	main()
