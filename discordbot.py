import discord
import datetime
import os
import re

from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')  

@client.command()
async def how(ctx2):
  help1 = discord.Embed(title="🐟🐟🐟使い方🐟🐟🐟",color=0xe74c3c,description=".start 回戦数 全組数: 全〇組で〇回戦開始\n---start後---\n集計ツールのコピペを貼り付け→自動で組数と通過者リストを読み込んで表示(コピペ通りに張り付けられてないとメンション)。全組集計が出そろったら終了\end: 強制終了")
  await ctx2.send(embed=help1)

@client.command()
async def start(ctx3,round,total):
  list4 = []
  for i in range(1,int(total)+1):
    list4.append(i)
  #print(list4)
  name= '{}回戦'.format(round)
  #print(name)
  #await ctx3.send("{}回戦 全{}組".format(round,total))
  remain = discord.Embed(title="{}回戦 全{}組".format(round,total),colour=0xe74c3c)
  remain.add_field(name="結果未提出組",value=list4, inline=True)
  now = await ctx3.send(embed=remain)

  next = ''
  n=1
  remain2 = discord.Embed(title="{}回戦".format(round),colour=0xe74c3c)
  remain2.add_field(name="通過者リスト{}".format(n),value=None, inline=True)
  now2 = await ctx3.send(embed=remain2)
  
  while len(list4) != 0:
    result = await client.wait_for('message')
    if result.guild.id == ctx3.guild.id:
        #print(result.content[0:6])

        if result.content.startswith(round):
        #if res.startswith == name:
          ns=result.content[1:6] 
          num = re.sub("\\D", "", ns)
          if int(num) in list4:

            a = result.content.find('主催コピペ用')
            #print (a)
            #print(len(result.content))
            #print(result.content[0:6])
            #print(result.content[a+len('主催コピペ用'):])
            if a == -1:
              await result.add_reaction('🤔')
              await ctx3.send("主催コピペ用は正しいですか？{}".format(result.author.mention))
            else:
              list4.remove(int(num))
              #print(list4)
              await result.add_reaction('🐟')
              remain = discord.Embed(title="{}回戦 全{}組".format(round,total),colour=0xe74c3c)
              remain.add_field(name="結果未提出組@{}".format(len(list4)),value=list4, inline=True)
              await now.edit(embed=remain)

              if len(next)+len(result.content[a+len('主催コピペ用'):]) >= 1000:
                remain2 = discord.Embed(title=f"{round}回戦",colour=0xe74c3c)
                remain2.add_field(name="通過者リスト{}".format(n),value=next, inline=True)
                await ctx3.send(embed=remain2)
                next = '' 
                n+=1

              next = next + result.content[a+len('主催コピペ用'):]
              #print(len(result.content[a+len('主催コピペ用'):]))
              #print(next)
              remain2 = discord.Embed(title=f"{round}回戦",colour=0xe74c3c)
              remain2.add_field(name="通過者リスト{}".format(n),value=next, inline=True)
              await now2.edit(embed=remain2)

        if result.content == 'end':
          if result.author.id == ctx3.author.id:
            break

        remain = discord.Embed(title="{}回戦 全{}組 終了".format(round,total),colour=0xe74c3c)
        await now.edit(embed=remain)
        await ctx3.send("全組集計投稿終了 {} @everyone".format(ctx3.author.mention))

token = os.environ['DISCORD_BOT_TOKEN']
client.run(token)
