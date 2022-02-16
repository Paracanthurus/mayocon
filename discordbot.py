import discord
import setting as S
import sys
import datetime
import traceback

client = discord.Client()

@client.event
async def on_ready():
	try:
		channel = client.get_channel(int(S.discordbot_channel_id))
		await channel.send(sys.argv[1])
	except Exception:
		errlog = open(S.Dir_path + '/err/' + str(datetime.datetime.now()), 'w')
		msg = traceback.format_exc()
		errlog.write(msg)
		errlog.close()
		print(msg + '\nエラーが発生しました\n')
	finally:
		await client.close()

client.run(S.discordbot_token)
