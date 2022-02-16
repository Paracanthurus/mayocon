import create_contest
import schedule
import time


schedule.every().day.at('09:00').do(create_contest.main())

while True:
	schedule.run_pending()
	time.sleep(60)
