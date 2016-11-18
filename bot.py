import discord
import asyncio
from itertools import chain

client = discord.Client()
loop = asyncio.get_event_loop()
varlist = [] * 256
channels = [] * 256
nationstats = [] * 256
chilestats = [] * 10
polandstats = [] * 10
constantinoplestats = [] * 10
chinastats = [] * 10
kilwastats = [] * 10
sumerstats = [] * 10
hellstats = [] * 10
australistats = [] * 10
burmastats = [] * 10
riostats = [] * 10
nuukstats = [] * 10
fsastats = [] * 10
consolechannel = ""
@client.event

async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	updateadmins()

def updateadmins():
	with open('admin', 'r') as file:
		global author
		global varlist
		author = file.read()
		author = author.split()
		varlist.insert(0, author)
		print('Admins updated successfully.')
		updatenations()

def updatenations():
	with open('nations', 'r') as file:
		global nation
		global varlist
		nation = file.read()
		nation = nation.split()
		varlist.insert(1, nation)
		print("Nations updated successfully.")
		updatenationstats()
		
def updatenationstats():
	with open('nationstats', 'r') as file:
		global nationstats
		global chilestats
		global polandstats
		global constantinoplestats
		global chinastats
		global kilwastats
		global sumerstats
		global hellstats
		global australiastats
		global burmastats
		global riostats
		global nuukstats
		global fsastats
		global varlist
		nationstats = file.read()
		nationstats = nationstats.split()
		nationstats[0:19] = []
		varlist.insert(2, nationstats)
		chilestats = nationstats[0:9]
		varlist.insert(3, chilestats)
		polandstats = nationstats[10:19]
		varlist.insert(4, polandstats)
		constantinoplestats = nationstats[20:29]
		varlist.insert(5, constantinoplestats)
		chinastats = nationstats[30:39]
		varlist.insert(6, chinastats)
		kilwastats = nationstats[40:49]
		varlist.insert(7, kilwastats)
		sumerstats = nationstats[50:59]
		varlist.insert(8, sumerstats)
		hellstats = nationstats[60:69]
		varlist.insert(9, hellstats)
		australiastats = nationstats[70:79]
		varlist.insert(10, australiastats)
		burmastats = nationstats[80:89]
		varlist.insert(11, burmastats)
		riostats = nationstats[90:99]
		varlist.insert(12, riostats)
		nuukstats = nationstats[100:109]
		varlist.insert(13, nuukstats)
		fsastats = nationstats[110:119]
		varlist.insert(14, fsastats)
		print("Nation stats updated successfully.")
		updateconsoleoutputchannel()
		
def updateconsoleoutputchannel():
	global consolechannel
	with open('consolechan', 'r+') as file:
		consolechannel = file.readlines()
		consolechannel = " ".join(consolechannel)
		consolechannel = client.get_channel(consolechannel)
	varlist.insert(15, consolechannel)
	print("Console output channel set successfully.")
	
async def print_console_channel(content):
	global consolechannel
	if consolechannel != "":
		await client.send_message(consolechannel, content)
	else:
		print("Error: Console channel not defined!")
	
@client.event
async def on_message(message):
	if message.content.startswith('%test'):
		await client.send_message(message.channel, message.author.id)
	elif message.content.startswith('%exit'):
		await client.send_message(message.channel, 'Please input shutdown code via direct message.')
		await client.send_message(message.author, 'Please input the shutdown code.')
	elif message.content.startswith('Lay down thy packet, and go to sleep.'):
		if message.author.id in author:
			if message.channel.is_private:
				await client.send_message(message.author, 'Shutting down.')
				print('Shutdown code detected.')
				await client.logout()
				await client.close()
			else:
				await client.send_message(message.author, 'Shutdown command is only accepted through direct message.')
	elif message.content.startswith('%addadmin'):
		if message.author.id in author or message.author.id == '174827375639396352':
			tmp = message.raw_mentions
			tmp = " ".join(tmp)
			print(tmp)
			with open('admin', 'a') as file:
				file.write(tmp + '\n')
			updateadmins()
	elif message.content.startswith('%debugvar'):
		tmp = str(message.content)
		if tmp.startswith('%debugvar'):
			tmp = tmp[10:]
			tmp = int(tmp)
			await print_console_channel(varlist[tmp])
	elif message.content.startswith('%listchannels'):
		for channel in message.server.channels:
			print(channel)
	elif message.content.startswith('%channelid'):
		await client.send_message(message.channel, message.channel.id)
	elif message.content.startswith('%addchannel'):
		global channels
		channels.append(message.channel)
		await client.send_message(message.channel, "Channel added successfully.")
	elif message.content.startswith('%relay'):
		tmp = str(message.content)
		tmp = tmp[7:]
		tmp = "".join(tmp)
		print("First split: " + tmp)
		tmp2 = tmp.split()
		if tmp2[0] in nation:
			tmp3 = tmp2[0]
			tmp2 = " ".join(tmp2)
			tmp2 = tmp2.replace(tmp3, "")
			print("Contents of tmp2: " + tmp2)
			for channel in channels:
				print(channel)
				await client.send_message(channel, "Message from " + tmp3 + ":" + tmp2)
	elif message.content.startswith("%about"):
		await client.send_message(message.channel, "Things about me:" + "\n" + "Preferred name: Ophelia" + "\n" + "Invoker: %" + "\n" + "Invite link: https://discordapp.com/oauth2/authorize?client_id=248240386869297155&scope=bot&permissions=0")
	elif message.content.startswith("%setconsolechannel"):
		global consolechannel
		if message.author.id in author or message.author.id == '174827375639396352':
			tmp3 = message.channel.id
			await client.send_message(message.channel, "Console channel set successfully.")
			with open('consolechan', 'r+') as file:
				file.write(tmp3)
			updateconsoleoutputchannel()
	elif message.content.startswith("%echo"):
		if message.author.id != client.user.id:
			await print_console_channel(message.content)
	elif message.content.startswith("%genserverentry"):
			with open(message.server.id, "w") as file:
				tmp = message.channel
				tmp2 = message.author
				await client.send_message(tmp, "Set your server's relay channel using %setrelaychannel.")
				tmp = client.wait_for_message(timeout=60, channel=message.channel, author=tmp2, content="%setrelaychannel")
				print(message.author.server_permissions.administrator)
				if message.author.server_permissions.administrator:
					file.write(message.channel.id)
					await client.send_message(message.channel, "This channel has been set as the relay channel.")
client.run('MjQ4MjQwMzg2ODY5Mjk3MTU1.Cw3Q_Q.AgwD4S6h3SrnDXG2H6Utrgwo11k')
