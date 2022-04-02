import discord
import setting as S
import sys
import datetime
import traceback

client = discord.Client()

@client.event
async def on_ready():
	try:
		if sys.argv[1] == 'err':
			user = await client.fetch_user(int(S.user_id))
			await user.send(str(datetime.datetime.now()) + '\nエラーが発生しました')
		else:
			channel = client.get_channel(int(sys.argv[2]))
			await channel.send(sys.argv[1])
	except Exception as e:
		errlog = open(S.Dir_path + '/err/' + str(datetime.datetime.now().date()) + '.log', 'a')
		msg = traceback.format_exc() + '\n' + str(e)
		errlog.write('\n' + str(datetime.datetime.now()) + '\n')
		errlog.write(msg + '\n')
		errlog.close()
		print(msg + '\nエラーが発生しました\n')
	finally:
		await client.close()

client.run(S.discordbot_token)
