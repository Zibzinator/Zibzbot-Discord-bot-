import time
import json
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.utils import get
import asyncio
import youtube_dl
import os
bot = commands.Bot(command_prefix="!")
server_name = "Zobz Kingdom"


queue = []

def remove_song(queue):
	if len(queue) >= 1:
		del queue[0]
	else:
		pass
		
def add_to_queue(queue, song):
	queue.append(song)

def is_connected(ctx):
	voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
	return voice_client and voice_client.is_connected()

def findID(nameId):
	json_file = open("userlist.json", "r", encoding="utf-8")
	y = json.load(json_file)
	for i in y["Users"]:
		if nameId == i["Id"]:
			return True
	json_file.close()
def findBot(nameId):
	json_file = open("userlist.json", "r", encoding="utf-8")
	y = json.load(json_file)
	for i in y["Users"]:
		if nameId == i["Id"]:
			if i["bot"]:
				return True
	json_file.close()
def findMod(nameId):
	json_file = open("userlist.json", "r", encoding="utf-8")
	y = json.load(json_file)
	for i in y["Users"]:
		if nameId == i["Id"]:
			if i["mod"]:
				return True
	json_file.close()


def add_todb(nameId):
	json_file = open("userlist.json", "r", encoding="utf-8")
	y = json.load(json_file)
	temp_list=[]
	for i in y["Users"]:
		names = i["Id"]
		nameId = str(nameId)
		temp_list.append(names)
	if nameId not in temp_list:
		new_use = {"Id": nameId,"bot": False,"mod": False}
		y["Users"].append(new_use)
		with open("userlist.json", "w") as f:
			json.dump(y, f, indent=2)
	else:
		pass



logVoice = 1

# Commands------------------------------------------------------------------

@bot.command()
async def spam(ctx):
	user = str(ctx.author)
	if findBot(user):
		for x in range(0, 4):
			await join(ctx)
			time.sleep(0.2)
			await leave(ctx)
	else:
		pass
@bot.command(aliases=["t"])
async def testyt (ctx):
	user = ctx.author
	add_todb(user)

@bot.command(aliases=["tj"])
async def testjoin(ctx):
	user = str(ctx.author)
	if findID(user):
		await ctx.send("You are in the database")
	else:
		await ctx.send("you are not in the data base so there fore you have no permission")		
	if findBot(user):
		await ctx.send("You have permissions to abuse me daddy")
	else:
		await ctx.send("You dont have permission to toch me ")

@bot.command(aliases=["j"])
async def join(ctx):
	user = ctx.author
	add_todb(user)
	try:
		try:
			channel = ctx.author.voice.channel
			await channel.connect()
			print("Joining '"+ str(ctx.author.voice.channel) +"' Summond by: '" + str(ctx.author)+"'!")
		except:
			await ctx.voice_client.move_to(channel)
			print("Joining '"+ str(ctx.author.voice.channel) +"' Summond by: '" + str(ctx.author)+"'!")
	except:
		
		uM = str(ctx.author.mention)
		uC = str(ctx.author)
		await ctx.send("Where you att " + uM +" I dont see you in any voice channel.")
		print("User: " + uC + " is trying to call the bot to join without being in voice channel")
				
			

@bot.command(aliases=["l"])
async def leave(ctx):
	try:
		await ctx.voice_client.disconnect()
		print("disconnecting from voice channel")

	except:
		uM = str(ctx.author.mention)
		uC = str(ctx.author)
		print("no")
		await ctx.send("There is nothing to disconnect from. " + uM + " is a dumbfuck!")
		print("User: " + uC + " is trying disconnect the bot")


@bot.command()
async def test(ctx):
	print("hello")
	
@bot.command()
async def shutdown(ctx):
	try:
		await ctx.voice_client.disconnect()
	except:
		print("boy")


@bot.command(aliases=["q"])
async def queue (ctx, url: str, queue):
	add_to_queue(url)

	
@bot.command(aliases=["p"])
async def play (ctx,url: str):
	user = str(ctx.author)
	add_todb(user)
	if findBot(user):
			await join(ctx)
			if is_connected(ctx):
				global voice
				song_there = os.path.isfile("song.mp3")
				try:
					print("removeing")
					if song_there:
						os.remove("song.mp3")
						print("removeing old song")
				except :
					print("permissionError")
					await ctx.send("Big nono")
					return
				
				voice = get(bot.voice_clients)

				ydl_opts = {
			        'format': 'bestaudio/best',
			        'postprocessors': [{
			            'key': 'FFmpegExtractAudio',
			            'preferredcodec': 'mp3',
			            'preferredquality': '192',
			        }],
			    }
				with youtube_dl.YoutubeDL(ydl_opts) as ydl:
					await ctx.send("Preparing the youtubelink.....")
					print("Downloading audio now\n")
					ydl.download([url])


				for file in os.listdir("./"):
					if file.endswith(".mp3"):
						name = file
						print(f"Renamed File: {file}\n")
						os.rename(file, "song.mp3")

				

				voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:print(" Done playing"))
				voice.source = discord.PCMVolumeTransformer(voice.source)
				voice.source.volume = 0.1

				nname = name.rsplit("-", 2)
				await ctx.send(f"Playing: {nname[0]}")
				print(f"Playing: {nname[0]}")
			else:
				await ctx.send(f"{ctx.author.mention} You cant use the play function without being in a voice channel")
	else:
			await ctx.send(f"{ctx.author.mention} You dont have permissionto use the play function")
	
@bot.command()
async def stop(ctx):
	voice.stop()
@bot.command()
async def pause(ctx):
	voice.pause()
	await ctx.send(f"Song pause by {ctx.author.mention}")
@bot.command()
async def resume(ctx):
	voice.resume()
# Bot events------------------------------------------------------------

@bot.event
async def on_ready():

	await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Pornhub.com/ToastBoy"))
	bot_ready = 1
	print("-----------------------------------------------")
	print("Hello")
	print("Zibz-bot initialized!")
	print("Bot is now ready")
	print("-----------------------------------------------")

@bot.event
async def on_member_join(member):
	add_todb(member)
	embed = discord.Embed(title="Rules of this discord server", description=" ‎", colour=0x23D160)
	embed.add_field(name="1)",value=" Be respectful", inline=False)
	embed.add_field(name="2)",value=" Sending/Linking any harmful material such as viruses, IP grabbers or harmware results in an immediate and permanent ban.", inline=False)		
	embed.add_field(name="3)",value=" the use of extreme language or any language that can come across as racist is strictly forbidden", inline=False)		
	embed.add_field(name="4)",value=" Usage of excessive extreme language that can be considered offensive is strictly forbidden", inline=False)
	embed.add_field(name="5)",value=" mentioning @everyone, the Moderators or a specific person without proper reason is prohibited.", inline=False)
	embed.add_field(name="6)",value=" Post content in the correct channels.", inline=False)
	embed.add_field(name="7)",value=" Don't post someone's personal information without that persons permission.", inline=False)
	embed.add_field(name="8)",value=" Listen to what Staff says.", inline=False)
	embed.add_field(name="9)",value=" arguing with an admins decision may result in a cool down.", inline=False)
	embed.add_field(name="10)",value=" Do not post graphic pictures of minors (<18yo)", inline=False)
	embed.add_field(name="11)",value=" Most importantly have FUN!!!", inline=False)
	embed.add_field(name=" ‎",value=" Type 'ACCEPT' if you understan and accept the rules of 'The Comunity' server", inline=False)
	embed.set_thumbnail(url="https://image.shutterstock.com/image-photo/knight-sword-shield-600w-762608260.jpg")
	embed.set_footer(text="-GateKeeper", icon_url=f"{member.guild.icon_url}")
	await member.send(content=None, embed=embed)
	
	def check(m):
		return m.content == str("ACCEPT")

	msg = await bot.wait_for('message', check=check)
	roll = discord.utils.get(member.guild.roles, name='It worked')
	await member.add_roles(roll)
	await member.send("Welcome " +str(member) + " to the " + server_name)
	print(f"{member} a person Just join the server")

bot.run("NjY1OTQ1ODUyOTQxOTU5MjAw.Xh9nUw.3XJp9MIosio92r-kXZtiqNVxJqk")