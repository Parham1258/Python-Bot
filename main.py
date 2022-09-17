import asyncio
import disnake as discord
import random
import os
import datetime, time
from replit import db
from disnake.ext import commands
from server import keep_alive

bot = commands.Bot(command_prefix = lambda bot, msg: (commands.when_mentioned_or(db['prefix'][str(msg.guild.id)]) if msg.guild != None else commands.when_mentioned_or('pb!'))(bot, msg), intents=discord.Intents.all()) #, test_guilds = [908099219401883670, 823959191894491206, 866689038731313193, 916407122474979398, 926443840632676412, 858300189358293037, 900579811544670218, 902248677891010641, 968171159776559174, 902970942173626378, 995060155848851537, 843562496543817778, 1004796648641273856]

class EmbedMinimalHelp(commands.MinimalHelpCommand):
  async def send_pages(self):
    destination = self.get_destination()
    for page in self.paginator.pages:
      e = discord.Embed(description = page, color = random.randint(0, 16777215))
    await destination.send(embed = e)

bot.help_command = EmbedMinimalHelp()

#on message event thing
@bot.event
async def on_message(message):
  if message.guild != None:
    if str(message.guild.id) not in db['prefix']:
      db['prefix'][str(message.guild.id)] = 'pb!'
  if str(message.author.id) in db["afk"]:
    del db["afk"][str(message.author.id)]
    await message.channel.send(f"Welcome back, {message.author.mention}", delete_after = 5)
  for member in message.mentions:
    if str(member.id) in db["afk"]:
      e = discord.Embed(title = f"{member.name} is AFK", description = f"Reason: {db['afk'][str(member.id)]['reason']}\nSince: <t:{db['afk'][str(member.id)]['time']}:R>", color = random.randint(0, 16777215))
      await message.channel.send(embed = e)
  await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
  try:
    if str(message.guild.id) in db["serversetting"]["gpd"]:
      if message.mentions:
        if not message.author.bot:
          e = discord.Embed(title = "Ghost ping detected!", description = f"{message.content}", color = random.randint(0, 16777215))
          e.set_footer(text = f"Message from: {message.author}")
          await message.channel.send(embed = e)
  except: pass

#when connected event lol
@bot.event
async def on_connection():
  bot.launch_time = datetime.datetime(1970, 1, 1)
  
#when bot is online event
@bot.event
async def on_ready():
  print("bot connected")
  await bot.change_presence(status = discord.Status.online, activity = discord.Game("Restarted"))
  bot.launch_time = datetime.datetime.utcnow()
  await asyncio.sleep(3)
  await bot.change_presence(status = discord.Status.online, activity = discord.Game("/ | Made in Python 3.8.2!"))
  """while True:
    print(f"{int(time.time())}")
    if len(db["reminders"]) == 1:
      check = 1
    else:
      check = 0
    for i in range(len(db["reminders"]) - check):
      if int(time.time()) >= db["reminders"][list(db["reminders"].keys())[i]]["time"]:
        ruser = db["reminders"][list(db["reminders"].keys())[i]]["rid"]
        rtext = db["reminders"][list(db["reminders"].keys())[i]]["rtext"]
        e = discord.Embed(title = "Reminder", description = f"{rtext}", color = random.randint(0, 16777215))
        await bot.get_user(ruser).send(embed = e)
        del db["reminders"][list(db["reminders"].keys())[i]]
    await asyncio.sleep(10)"""

#load extension command
@bot.command(aliases = ["l"], help = "load extension", description = "bot owner only\nusage: ?load (extension)", hidden = True)
@commands.is_owner()
async def load(ctx, extension):
  bot.load_extension(f"cogs.{extension}")
  await ctx.send(f"cogs.{extension} is loaded")
  
#reload extension command
@bot.command(aliases = ["rl"], help = "load extension", description = "bot owner only\nusage: ?reload (extension)", hidden = True)
@commands.is_owner()
async def reload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")
  bot.load_extension(f"cogs.{extension}")
  await ctx.send(f"cogs.{extension} is reloaded")

#unload extension command
@bot.command(aliases = ["ul"], help = "load extension", description = "bot owner only\nusage: ?unload (extension)", hidden = True)
@commands.is_owner()
async def unload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")
  await ctx.send(f"cogs.{extension} is unloaded")

#load cogs
for filename in os.listdir('./cogs'):   
  if filename.endswith('.py') and filename not in []:
    bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive() # Keeps alive the bot thing
bot.run(os.getenv('TOKEN'))