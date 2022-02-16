
#### 自分で入力してね ####


### プログラム設定 ###
username_github = ''
password_github = ''

chromedriver_path = ''
# chromedriverの絶対パス

discordbot = True
# botを使用する
discordbot_token = ''
discordbot_channel_id = 1234567890

Timelimit_Find_problems = 300
# 問題の決定に n秒以上かかった場合プログラムを停止

Del_logfile_span = 180
# n日以上前のログファイルを自動削除



### テスト用設定 ###
No_create_contest = True
# コンテストを作成せずに終了
bot_off = True
# botを起動せずに終了
Display_Browser = True
# 実行時にブラウザを表示する



### コンテスト設定 ###
Contest_Title = ''
Description = ''

Public_State = 2
# 1:Public  2:Private
Mode = 1
# 1:Nomal  2:Lockout  3:Training
Penalty = 300

Start_Day = 0
# n日後 (今日なら Start_Day = 0)
Start_Time = '21:00'
Duration = 100

Expected_Participants = ''

Exclude_experimental_difficulty = True

Exclude_probrems = 4
# 1: Exclude all the solved problems by expected participants
# 2: Exclude all the submitted problems by expected participants
# 3: Exclude all the solved problems in last 6 months by expected participants
# 4: Exclude all the solved problems in last 4 weeks by expected participants
# 5: Exclude all the solved problems in last 2 weeks by expected participants
# 6: Exclude all the solved problems in last 7 days by expected participants
# 7: Don't exclude solved problems by expected participants

Problems = [
	(0, 400),
	(0, 400),
	(400, 800),
	(800, 1200),
	(1200, 1600),
	(1600, 2000)
]

Points = [100, 200, 300, 400, 500, 600]

Sort_Difficulty = True

ABC_Only = True

Exclude_past_days = 30
# 過去 n日間に出題された問題を除外（./log/ のファイル参照)

No_contest_day_ABC = True
# ABCのある日はコンテストを作成しない
No_contest_day_ARC = True
# ARCのある日はコンテストを作成しない
