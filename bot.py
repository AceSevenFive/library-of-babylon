import discord
import asyncio
import os.path
from itertools import chain
import itertools

client = discord.Client()
loop = asyncio.get_event_loop()
varlist = [] * 256
consolechannel = ""
nations = [] * 256
@client.event

async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	updateadmins()
	updateconsoleoutputchannel()
	updatenations()

def updateadmins():
	global author
	global varlist
	global nationmods
	with open('admin', 'r') as file:
		author = file.read()
		author = author.split()
		varlist.insert(0, author)
		print('Admins updated successfully.')
	with open('nationmods', 'r') as file:
		nationmods = file.readlines()
		varlist.insert(1, nationmods)
		print("Nation mods updated successfully.")
		
def updateconsoleoutputchannel():
	global consolechannel
	with open('consolechan', 'r+') as file:
		consolechannel = file.readlines()
		consolechannel = " ".join(consolechannel)
		consolechannel = client.get_channel(consolechannel)
	varlist.insert(3, consolechannel)
	print("Console output channel set successfully.")
	
def updatenations():
	global nations
	with open('nations', "r") as file:
		nations = file.read()
	print("Nations read successfully.")
	varlist.insert(4, nations)
	
async def addnation(name):
	with open("nations", "a") as file:
		file.write("\n" + name)
		updatenations()
	await print_console_channel("New nation added: " + name, 2)
	
async def print_console_channel(content, messagetype):
	global consolechannel
	if consolechannel != "":
		if messagetype == 1:
			await client.send_message(consolechannel, "[CONSOLE] " + content)
		elif messagetype == 2:
			await client.send_message(consolechannel, "[INFO] " + content)
		elif messagetype == 3:
			await client.send_message(consolechannel, "[INTERNAL] " + content)
		elif messagetype == 4:
			tmp666 = await client.get_user_info("174827375639396352")
			await client.send_message(consolechannel, "[ALERT] " + tmp666.mention + ": " + content)
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
			await print_console_channel(str(varlist[tmp]), 1)
	elif message.content.startswith('%listchannels'):
		for channel in message.server.channels:
			print(channel)
	elif message.content.startswith('%channelid'):
		await client.send_message(message.channel, message.channel.id)
	elif message.content.startswith('%relay'):
		tmp = str(message.content)
		tmp = tmp[7:]
		tmp = "".join(tmp)
		print("First split: " + tmp)
		tmp2 = tmp.split()
		if tmp2[0] in nations:
			tmp3 = tmp2[0]
			tmp2 = " ".join(tmp2)
			tmp2 = tmp2.replace(tmp3, "")
			tmp2 = tmp2.split()
			print("Second split: " + str(tmp2))
			if tmp2[0] in nations:
				tmp11 = tmp2[0]
				with open(tmp11, "r") as file:
					tmp4 = file.readlines()
					tmp4 = "".join(tmp4)
					tmp4 = tmp4.replace("\n", " ")
					tmp4 = "".join(tmp4)
					tmp4 = tmp4.split()
					tmp8 = tmp4
					tmp7 = tmp4[tmp4.index("-RELAYCHANNEL-"):tmp4.index("-RELAYAUTHUSERS-")]
					print(str(tmp4))
					tmp7.remove("-RELAYCHANNEL-")
					tmp7.remove("&&&&&")
					tmp7 = "".join(tmp7)
				with open(tmp3, "r") as file:
					tmp12 = file.readlines()
					tmp12 = "".join(tmp12)
					tmp12 = tmp12.replace("\n", " ")
					print(str(tmp12))
					tmp6 = tmp12[tmp12.index("-RELAYAUTHUSERS-"):tmp12.index("-ENDOFSTATS-")]
					tmp6 = tmp6.split()
					tmp6.remove("-RELAYAUTHUSERS-")
					tmp6 = "".join(tmp6)
				tmp9 = str(message.author.id)
				print(tmp9)
				print(tmp6)
				if tmp9 in tmp6:
					tmp5 = client.get_channel(tmp7)
					tmp2 = " ".join(tmp2)
					tmp2 = tmp2.replace(tmp11, "")
					await client.send_message(tmp5, "Message from " + tmp3 + ":" + tmp2)
				else:
					await client.send_message(message.channel, "Error: You are not authorized to send relay messages.")
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
			await print_console_channel(message.content, 1)
	elif message.content.startswith("%gennationentry"):
		if message.author.id in nationmods or message.author.id == "174827375639396352":
			await client.send_message(message.channel, "Follow these instructions to generate a nationfile:" + "\n" + "Type %setnationstats with the following arguments in this order:")
			await client.send_message(message.channel, "Name, Vassal Of, Treasury, GPT, Friendships, Open Borders, Alliances, Defensive Pacts, Denouncing, War.")
			await client.send_message(message.channel, "If multiple names are on a line, separate them with slashes (ie Chile/Poland).")
			tmp = await client.wait_for_message(timeout=60, channel=message.channel, author=message.author)
			tmp = str(tmp.content)
			tmp2 = tmp.split()
			print(str(tmp2))
			if tmp2[0].startswith("%setnationstats"):
				tmp2.remove("%setnationstats")
				tmp3 = tmp2[0]
				tmp2 = " ".join(tmp2)
				with open(tmp3, "w") as file:
					tmp3 = tmp3.split()
					print(str(tmp3))
					tmp2 = tmp2.split()
					file.close()
				with open(tmp3[0], "a") as file:
					file.write("-NATIONSTATS-" + "\n")
					for stat in tmp2:
						file.write(stat + "\n")
					file.write("&&&&&" + "\n")
					file.write("-LOCALNATIONMODS-" + "\n")
				if tmp3[0] not in nations:
					await addnation(tmp3[0])
				await client.send_message(message.channel, "Now, send %setlocalnationmods and @mention a list of people you want to be able to mod your nation's bot stuff.")
				tmp = await client.wait_for_message(timeout=60, channel=message.channel, author=message.author)
				tmp7 = tmp.raw_mentions
				tmp = str(tmp.content)
				tmp2 = tmp.split()
				print(str(tmp2))
				if tmp2[0].startswith("%setlocalnationmods"):
					tmp2.remove("%setlocalnationmods")
					tmp5 = " ".join(tmp7)
					tmp5 = tmp5.split()
					print(tmp5)
					with open(tmp3[0], "a") as file:
						for user in tmp5:
							file.write(str(user))
							file.write("\n")
						file.write("&&&&&" + "\n")
				await client.send_message(message.channel, "Now, send %setrelaychannel in the channel you want to have incoming messages sent to. Make sure I can see it.")
				tmp = await client.wait_for_message(timeout=60, author=message.author, content="%setrelaychannel")
				with open(tmp3[0], "a") as file:
					file.write("-RELAYCHANNEL-")
					file.write("\n" + str(tmp.channel.id) + "\n")
					file.write("&&&&&")
					file.write("\n" + "-RELAYAUTHUSERS-" + "\n")
				await client.send_message(message.channel, "Now, send %setrelayauth and mention a list of people you want to be able to use the relay on your nation's behalf.")
				tmp = await client.wait_for_message(timeout=60, author=message.author)
				tmp8 = tmp.raw_mentions
				tmp = str(tmp.content)
				tmp9 = tmp.split()
				if tmp9[0].startswith("%setrelayauth"):
					tmp9.remove("%setrelayauth")
					tmp10 = " ".join(tmp8)
					tmp10 = tmp10.split()
					with open(tmp3[0], "a") as file:
						for user in tmp10:
							file.write(str(user))
							file.write("\n")
						file.write("-ENDOFSTATS-")
						file.write("\n" + "&&&&&")
				await client.send_message(message.channel, "All done!")
	elif message.content.startswith("%addnationmod"):
		if message.author.id in author or message.author.id == '174827375639396352':
			global nationmods
			tmp = message.raw_mentions
			if tmp not in nationmods:
				tmp = " ".join(tmp)
				print(tmp)
				with open('nationmods', 'a') as file:
					file.write(tmp + '\n')
				await client.send_message(message.channel, "Successfully added user to global nation mods list.")
				await print_console_channel("User added as nation mod.", 2)
				updateadmins()
			else:
				await client.send_message(message.channel, "That user is already a global nation mod.")
		else:
			await client.send_message(message.channel, "You do not have permission to execute this command.")
			await print_console_channel("Attempt at %addnationmod from" + message.raw_mentions, 4)
	elif message.content.startswith("%removenationmod"):
		if message.author.id in author or message.author.id == "174827375639396352":
			tmp = message.raw_mentions
			tmp = "".join(tmp)
			global nationmods
			if str(nationmods).find(tmp) != -1:
				tmp2 = " ".join(tmp)
				with open("nationmods", "r") as file:
					tmp2 = file.readlines()
				tmp2.remove(tmp + "\n")
				tmp2 = "".join(tmp2)
				with open("nationmods", "w") as file:
					file.write(tmp2)
				await client.send_message(message.channel, "That user is no longer a global nation mod.")
			else:
				await client.send_message(message.channel, "That user is not a global nation mod.")
		else:
			await client.send_message(message.channel, "You do not have permission to execute this command.")
			await print_console_channel("Attempt at %removenationmod from" + message.raw_mentions, 4)
	elif message.content.startswith("%liststaff"):
		tmp = str(message.content)
		tmp = tmp[11:]
		tmp = "".join(tmp)
		tmp2 = tmp.split()
		if tmp2[0] == "nationmods":
			tmp2 = "".join(tmp2)
			print(tmp2)
			tmp2 = tmp2[10:]
			print(tmp2)
			tmp2 = tmp2.split()
			print(str(tmp2))
			if tmp2[0] == "global":
				with open("nationmods", "r") as file:
					tmp3 = file.read()
					tmp3 = tmp3.split()
					await client.send_message(message.channel, "List of global nation mods:")
					for user in tmp3:
						tmp4 = await client.get_user_info(user)
						await client.send_message(message.channel, tmp4)
			elif tmp2[0] in nations:
				with open(tmp2[0], "r") as file:
					tmp3 = file.read()
					tmp3 = tmp3.split()
					tmp3 = tmp3[tmp3.index("-LOCALNATIONMODS-"):tmp3.index("-RELAYCHANNEL-")]
					tmp3.remove("&&&&&")
					tmp3.remove("-LOCALNATIONMODS-")
					for user in tmp3:
						tmp3[tmp3.index(user)] = str(await client.get_user_info(user))
					tmp3 = "\n".join(tmp3)
					await client.send_message(message.channel, "List of nation mods for " + tmp2[0] + ":" + "\n" + tmp3)
		elif tmp2[0] == "admins":
			with open("admin", "r") as file:
				tmp3 = file.read()
				tmp3 = tmp3.split()
				await client.send_message(message.channel, "List of bot admins:")
				for user in tmp3:
					tmp4 = await client.get_user_info(user)
					await client.send_message(message.channel, tmp4)
	elif message.content.startswith("%shownationstats"):
		tmp = str(message.content)
		tmp = tmp[17:]
		tmp = "".join(tmp)
		tmp2 = tmp.split()
		if tmp2[0] in nations:
			with open(tmp2[0], "r") as file:
				tmp3 = file.read()
				tmp3 = tmp3.split()
				tmp3[0] = tmp3[0] + tmp3[1]
				tmp3[0] = []
				tmp3[1] = []
				await client.send_message(message.channel, "STATS FOR " + str(tmp3[1]) + ":" + "\n" + "Vassal of: " + str(tmp3[2]) + "\n" + "Treasury: " + str(tmp3[3]) + "\n" + "GPT: " + str(tmp3[4]) + "\n" + "Friendships: " + str(tmp3[5]) + "\n" + "Open Borders: " + str(tmp3[6]) + "\n" + "Alliances: " + str(tmp3[7]) + "\n" + "Defensive Pacts: " + str(tmp3[8]) + "\n" + "Denouncing: " + str(tmp3[9]) + "\n" + "War: " + str(tmp3[10]))
		else:
			await client.send_message(message.channel, "Invalid argument. Use %help shownationstats for help.")
client.run('MjQ4MjQwMzg2ODY5Mjk3MTU1.Cw3Q_Q.AgwD4S6h3SrnDXG2H6Utrgwo11k')
