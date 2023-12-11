import discord
import mysql.connector
import asyncio
from discord.ext import commands
import requests

host = 'host'
user = 'user'
password = 'password'
database = 'database'

mydb = mysql.connector.connect(host=host,
                               user=user,
                               password=password,
                               database=database)
mycursor = mydb.cursor()


Intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",
                   intents=Intents,
                   allowed_mentions=discord.AllowedMentions(everyone=True))

bot.remove_command("help")

role = 0
starter = []

@bot.event
async def on_ready():
  print("準備完了")

  try:
    if mydb.is_connected():
      print("MySQLデータベースに接続されました。")
    synced = await bot.tree.sync()
    print(f"{len(synced)}個のコマンドを同期しました。")
    guild = discord.utils.find(lambda g: g.id == 1081858313454637066,
                               bot.guilds)
    global role
    role = guild.get_role(1081886055323672577)
    print(role)
  except Exception as e:
    print(e)




@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    return
  if isinstance(error, commands.MissingRole):
    await ctx.channel.send("Reporter role is required!")


async def check_player(namelist):
  global mydb, mycursor
  for name in namelist:
    try:
      mydb.commit()
      mycursor.execute('SELECT name FROM player_info WHERE name = %s;', (name, ))
      n = mycursor.fetchall()
      if mycursor.rowcount == 1 and name == n[0][0]:
        None
      else:
        return False
    except:
      mydb = mysql.connector.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=database)
      mycursor = mydb.cursor()
      mydb.commit()
      mycursor.execute('SELECT name FROM player_info WHERE name = %s;', (name, ))
      n = mycursor.fetchall()
      if mycursor.rowcount == 1 and name == n[0][0]:
        None
      else:
        return False


async def get_cc(name):
  global mydb
  try:
    mydb.commit()
  except:
    mydb = mysql.connector.connect(host=host,
                               user=user,
                               password=password,
                               database=database)
    mydb.commit()
  mycursor.execute('SELECT countryCode FROM player_info WHERE name = %s;',
                   (name, ))
  cc = mycursor.fetchall()
  if mycursor.rowcount == 1:
    return cc[0][0]
  else:
    return "Error"

@bot.command(ignore_extra=True)
@commands.has_role("Reporter")
async def submit(ctx, tier:str, c1:str, s1:int, c2:str, s2:int):
  b = await ctx.channel.send("Working...")
  a = await check_player([c1, c2])
  if a != False:
    if s1 + s2 == 28:
      if s1 >= s2:
        clist = [c1, c2]
        slist = [s1, s2]
      else:
        clist = [c2, c1]
        slist = [s2, s1]
      tier_list = ["c", "b", "a", "unranked", "test"]
      if tier in tier_list:
        
        channel_dic = {
                       "c":1090888092103225384,
                       "b":1090888062940225536,
                       "a":1090887989338578974,
                       "unranked":1081888818791207013,
                      "test":1085550080494415884}
        result_channel = bot.get_channel(channel_dic[tier])
        cc1, cc2 = await asyncio.gather(get_cc(clist[0]), get_cc(clist[1]))
        url = f"https://gb.hlorenzi.com/table.png?data=1%20%231d6ade%0A{clist[0]}%20%5B{cc1}%5D%20{slist[0]}%0A2%20%234A82D0%0A{clist[1]}%20%5B{cc2}%5D%20{slist[1]}"
        response = requests.get(url)
        image = response.content
        with open("result.png", "wb") as f:
            f.write(image)
        await result_channel.send(
          content=f"{clist[0]} {slist[0]}\n{clist[1]} {slist[1]}",
          file=discord.File("result.png"))
        await b.delete()
        await ctx.channel.send(
          content=f"Successfully sent table to {result_channel.mention}")
      else:
        await b.delete()
        await ctx.channel.send(
          "Your tier is not valid. Correct tiers are: ['a', 'b', 'c', 'unranked']"
        )
    else:
      await b.delete()
      await ctx.channel.send("Total score should be 28 points!")
  else:
    await b.delete()
    await ctx.channel.send("mk1-name is incorrect!")


bot.run('token')
