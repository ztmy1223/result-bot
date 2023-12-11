import os
import discord
import mysql.connector
# import deepl
# import aiohttp
import asyncio
from discord.ext import commands
# from discord import app_commands
# from PIL import Image, ImageDraw, ImageFont
# from random import choice
import requests

from server import keep_alive

host = os.environ['host']
user = os.environ['user']
password = os.environ['password']
database = os.environ['database']

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


# @bot.command(ignore_extra=True)
# @commands.has_role("Reporter")
# async def submit2(ctx, tier: str, c1: str, s1: int, c2: str, s2: int):
#   # a = await check_player([c1, c2])
#   # if a != False:
#   if ctx.author.nick == c1 or ctx.author.nick == c2 or ctx.author.name == c1 or ctx.author.name == c2 or role in ctx.author.roles or ctx.author.global_name == c1 or ctx.author.global_name == c2:
#     # def check(reaction, user):
#     #   return user == ctx.author and str(reaction.emoji) == '☑'
#     if s1 + s2 == 28:
#       if s1 >= s2:
#         clist = [c1, c2]
#         slist = [s1, s2]
#       else:
#         clist = [c2, c1]
#         slist = [s2, s1]
#       if tier == "g":
#         result_channel = bot.get_channel(1090888234780872845)
#       elif tier == "f":
#         result_channel = bot.get_channel(1090888205722722454)
#       elif tier == "e":
#         result_channel = bot.get_channel(1090888159564410901)
#       elif tier == "all":
#         result_channel = bot.get_channel(1106912851295211530)
#       elif tier == "d":
#         result_channel = bot.get_channel(1090888125758328872)
#       elif tier == "c":
#         result_channel = bot.get_channel(1090888092103225384)
#       elif tier == "b":
#         result_channel = bot.get_channel(1090888062940225536)
#       elif tier == "a":
#         result_channel = bot.get_channel(1090887989338578974)
#       elif tier == "s":
#         result_channel = bot.get_channel(1090887950855843900)
#       elif tier == "x":
#         result_channel = bot.get_channel(1090887908505952326)
#       elif tier == "z":
#         result_channel = bot.get_channel(1090887876109156424)
#       elif tier == "unranked":
#         result_channel = bot.get_channel(1081888818791207013)
#       elif tier == "test":
#         result_channel = bot.get_channel(1085550080494415884)
#       else:
#         await ctx.channel.send(
#           "Your tier is not valid. Correct tiers are: ['z', 'x', 's', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'all', 'unranked']"
#         )
#         result_channel = 1

#       if result_channel != 1:
#         await ctx.channel.send("Working...", delete_after=0)
#         i = choice(['z', 'x', 's', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'free'])
#         pic_before = f'{i}.jpg'
#         pic_after = f'{i}r.jpg'
#         img = Image.open(pic_before)
#         font1 = ImageFont.truetype('FRAMD.TTF', 50)
#         font2 = ImageFont.truetype('FRAMD.TTF', 75)
#         font3 = ImageFont.truetype('FRAMD.TTF', 20)
#         draw = ImageDraw.Draw(img)
#         draw.text((550, 5), f'Tier-{tier}', 'white', font=font1)
#         draw.text((500, 275), f'{clist[0]}', 'white', font=font2, anchor='mm')
#         draw.text((770, 278), f'{slist[0]}', 'white', font=font2, anchor='mm')
#         draw.text((500, 475), f'{clist[1]}', 'white', font=font2, anchor='mm')
#         draw.text((770, 478), f'{slist[1]}', 'white', font=font2, anchor='mm')
#         draw.text((20, 23),
#                   f'submitted by {ctx.author.nick or ctx.author.name}',
#                   'white',
#                   font=font3)
#         img.save(pic_after)
#         pic = pic_after

#         await result_channel.send(
#           content=f"-\n{clist[0]} {slist[0]}\n{clist[1]} {slist[1]}",
#           file=discord.File(pic))
#         await ctx.channel.send(
#           content=f"Successfully sent table to {result_channel.mention}")
#       else:
#         None
#     else:
#       await ctx.channel.send("Total score should be 28 points!")
  # else:
  #   # ctx.channel.send("The name is not correct")
  #   None

    # result = await ctx.channel.send(content="Please react to this message with ☑ within the next 30 seconds to confirm the table is correct", file=discord.File(pic))
    # await result.add_reaction('☑')
    # try:
    #   reaction, user = await bot.wait_for("reaction_add", timeout=30, check=check)
    # except asyncio.TimeoutError:
    #   await result.delete()
    # else:
    #   await result.delete()



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
        with open("test.png", "wb") as f:
            f.write(image)
        await result_channel.send(
          content=f"{clist[0]} {slist[0]}\n{clist[1]} {slist[1]}",
          file=discord.File("test.png"))
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


# @bot.event
# async def on_raw_reaction_add(payload):
#   channel_id = payload.channel_id
#   if channel_id == 1082200486788210708:
#     emoji = payload.emoji
#     if type(emoji) != str:
#       emoji_id = emoji.id
#       if emoji_id == 1081894631077326899:
#         member = payload.member
#         roles = member.roles
#         if role in roles:
#           channel = bot.get_channel(channel_id)
#           message = await channel.fetch_message(payload.message_id)
#           name = message.content
#           await message.add_reaction("☑")
#           await message.author.edit(nick=name, roles=starter)
#         else:
#           print("not staff")
#       else:
#         print("not emoji")
#     else:
#       print("not emoji")



# API_KEY = os.environ['deepl_key'] # 自身の API キーを指定

# text = 'Riemann Zeta function is a very important function in number theory.'


# イニシャライズ
# translator = deepl.Translator(API_KEY)

# # 翻訳を実行
# result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)

# # print すると翻訳後の文章が出力される
# print(result)


# @bot.command()
# @commands.has_role("MK1 Staff")
# async def en(ctx):
#   # source_lang = 'JA'
#   target_lang = 'EN-GB'
#   message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
#   text = message.content
#   result = translator.translate_text(text, target_lang=target_lang)
#   await message.reply(result.text, mention_author=False)

# @bot.command()
# @commands.has_role("MK1 Staff")
# async def jp(ctx):
#   # source_lang = 'EN'
#   target_lang = 'JA'
#   message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
#   text = message.content
#   result = translator.translate_text(text, target_lang=target_lang)
#   await message.reply(result.text, mention_author=False)

# @bot.command()
# @commands.has_role("MK1 Staff")
# async def send(ctx, channel_id:int):
#   send_channel = bot.get_channel(channel_id)
#   message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
#   await send_channel.send(content=message.content)

# @bot.command()
# @commands.has_role("MK1 Staff")
# async def dmsend(ctx, player_id:int):
#   player = bot.get_user(player_id)
#   message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
#   await player.send(content=message.content)


# import time

# @bot.command()
# @commands.has_role("MK1 Staff")
# async def ztmy(ctx):
#   guild = discord.utils.find(lambda g: g.id == 1081858313454637066,
#                                bot.guilds)
#   for channel in guild.channels:
#     try:
#       last_msg = await channel.fetch_message(channel.last_message_id)
#       content = last_msg.content
#       print(f"[{channel}]\n{content}")
#       time.sleep(1)
#     except Exception as e:
#       print(f"[{channel}]\n{e}")
#       time.sleep(1)

keep_alive()
my_secret = os.environ['token']
bot.run(my_secret)
