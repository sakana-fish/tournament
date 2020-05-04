import discord
import datetime
import os
import re

from discord.ext import commands
import asyncio
import random

#list = []
#apre = 'おさかなのサーバー'


from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')  
    await client.change_presence(activity=discord.Game(name='おさかな天国'))

@client.command()
async def how(ctx2):
  help1 = discord.Embed(title="🐟🐟🐟使い方🐟🐟🐟",color=0xe74c3c,description=".start 回戦数 全組数: 全〇組で〇回戦開始\n---start後---\n集計ツールのコピペを貼り付け→自動で組数と通過者リストを読み込んで表示(コピペ通りに張り付けられてないとメンション※「主催者コピペ用」以降の文字を通過者リストに追加するため「お疲れさまでした」等の文字追加厳禁)。全組集計が出そろったら終了\nend→強制終了")
  await ctx2.send(embed=help1)

@client.command()
async def start(ctx3):
  def check(m):
    return m.author.id == ctx3.author.id

  setting = discord.Embed(title="大会概要\n",colour=0xe74c3c,description="大会の名前を入力してください")
  #setting.add_field(name=f"test",value="test\ntest{title}", inline=False)

  set = await ctx3.send(embed=setting) 
  tournamentname = await client.wait_for('message',check=check)
  tournamentname = tournamentname.content
  #await client.messsage.delete(tournamentname)

  setting = discord.Embed(title="大会概要\n",colour=0xe74c3c,description="大会の形式を入力してください。\n1:個人 2:タッグ 3:プルス 4:フォーマン 6:6v6")
  setting.add_field(name="大会名",value=tournamentname, inline=False)
  await set.edit(embed=setting)
  keishiki = await client.wait_for('message',check=check)
  keishiki = int(keishiki.content)

  setting = discord.Embed(title="大会概要\n",colour=0xe74c3c,description="大会参加者の人数を入力してください。")
  setting.add_field(name="大会名",value=tournamentname, inline=False)
  await set.edit(embed=setting)
  setting.add_field(name="形式 1:個人 2:タッグ 3:プルス 4:フォーマン 6:6v6",value=keishiki, inline=False)
  await set.edit(embed=setting)
  player = await client.wait_for('message',check=check)
  player = int(player.content)
  total = int(player/12)
  round = 1
  passnum1=[]
  passplus1=[]
  race1=[]
  total1 = [total]
  ok3 = 1
  while ok3 == 1:
    ok = 1
    ok2 = 1
    while ok2 == 1:
        setting = discord.Embed(title=f"{round}回戦の通過組数(個人の場合人数)を入力してください。",colour=0xe74c3c,description="大会名:{} 形式:{} 参加者数:{}名".format(tournamentname,keishiki,player))
        for i in range(round-1):
         # print("hello")
          a = (int(passnum1[i])*int(total1[i])+int(passplus1[i]))*keishiki
          setting.add_field(name=f"{i+1}回戦",value=f"通過組数:{passnum1[i]}組 得点上位:{passplus1[i]}組 レース数:{race1[i]}レース 通過人数:{a}", inline=False)
        await set.edit(embed=setting)
    
        #await ctx3.send("{}回戦の通過組数(個人の場合人数)を入力してください。".format(round))        
        while ok == 1:
          #print("q")
          tests = await client.wait_for('message',check=check)
          passnum1.append(tests.content)
          passnum = tests.content
              #if isinstance(passnum, int) == "True" and isinstance(survive, int) == "True":
          ok = 0
          #else await ctx3.send("try again")

        ok = 1

        setting = discord.Embed(title=f"{round}回戦の得点上位人数を入力してください。",colour=0xe74c3c,description="大会名:{} 形式:{} 参加者数:{}名".format(tournamentname,keishiki,player))
        for i in range(round-1):
          print("hello")
          #setting.add_field(name=f"{i+1}回戦",value=f"通過組数:{passnum1[i]}組 得点上位:{passplus1[i]}組 レース数:{race1[i]}レース 通過人数{passnum1[i]*keishiki+passplus1[i]}", inline=False)
          a = (int(passnum1[i])+int(passplus1[i]))*keishiki*int(total1[i+1])
          setting.add_field(name=f"{i+1}回戦",value=f"通過組数:{passnum1[i]}組 得点上位:{passplus1[i]}組 レース数:{race1[i]}レース 通過人数:{a}", inline=False)
        a = int(passnum1[round-1])*keishiki*int(total)
        if a%12 == 0:
          b=0
        else:
          b=12-a%12
        setting.add_field(name=f"{round}回戦",value=f"通過組数:{passnum1[round-1]}組 通過人数{a} 不足@{int(b/int(keishiki))}組", inline=False)
        await set.edit(embed=setting)

        #await ctx3.send("{}回戦の得点上位人数を入力してください。".format(round))
        while ok == 1:
          #print("q")
          tests = await client.wait_for('message',check=check)
          passplus1.append(int(tests.content))
          passplus = tests.content
              #passplus = int(passplus)
              #if isinstance(passnum, int) == "True" and isinstance(survive, int) == "True":
          ok = 0
          #else await ctx3.send("try again")
        if (int(total)*int(passnum)+int(passplus))*keishiki%12 == 0:
          ok2 = 0         

          setting = discord.Embed(title=f"{round}回戦のレース数を入力してください。",colour=0xe74c3c,description="大会名:{} 形式:{} 参加者数:{}名".format(tournamentname,keishiki,player))
          for i in range(round-1):
            #print("hello")
            setting.add_field(name=f"{i+1}回戦",value=f"通過組数:{passnum1[i]}組 得点上位:{passplus1[i]}組 レース数:{race1[i]}レース 通過人数:{(int(passnum1[i])*keishiki+int(passplus1[i]))*int(total)}", inline=False)
          
          a = (int(passnum1[round-1])*int(total)+int(passplus1[round-1]))*keishiki
          setting.add_field(name=f"{round}回戦",value="通過組数:{}組 得点上位:{}組 通過人数{}".format(passnum1[round-1],passplus1[round-1],a), inline=False)
          await set.edit(embed=setting)
           
          #await ctx3.send("{}回戦のレース数を入力してください。".format(round))
          tests = await client.wait_for('message',check=check)        
          race1.append(tests.content)
          round += 1
          if (int(total)*int(passnum)+int(passplus))*keishiki/12 == 1:
            ok3 = 0

            setting = discord.Embed(title="決勝戦のレース数を入力してください。",colour=0xe74c3c,description="大会名:{} 形式:{} 参加者数:{}名".format(tournamentname,keishiki,player))
            for i in range(round-1):
              #print("hello")
              setting.add_field(name=f"{i+1}回戦",value=f"通過組数:{passnum1[i]}組 得点上位:{passplus1[i]}組 レース数:{race1[i]}レース 通過人数:{(int(passnum1[i])*keishiki+int(passplus1[i]))*int(total)}", inline=False)          
            await set.edit(embed=setting)

            #await ctx3.send("決勝戦のレース数を入力してください。".format(round))
            tests = await client.wait_for('message',check=check)            
            race1.append(tests.content)    
            finalround = round
            setting = discord.Embed(title=f"{tournamentname}",colour=0xe74c3c,description="形式:{} 参加者数:{}名".format(keishiki,player))
            for i in range(round-1):
              #print("hello")
              setting.add_field(name=f"{i+1}回戦",value=f"通過組数:{passnum1[i]}組 得点上位:{passplus1[i]}組 レース数:{race1[i]}レース 通過人数:{(int(passnum1[i])*keishiki+int(passplus1[i]))*int(total)}", inline=False)
            setting.add_field(name=f"決勝戦",value=f"レース数:{race1[i+1]}レース", inline=False)     
            await set.edit(embed=setting)
          total=(int(total)*int(passnum)+int(passplus))*keishiki/12
          total=int(total)
          total1.append(total)
        else:
          #round -= 1        
          #total1.remove(total)
          #total=int(total)*12
          await ctx3.send("エラー:全体の通過人数が正しくありません")
          ok = 1

  tournament = discord.Embed(title=f"{tournamentname}",colour=0xe74c3c)
  tourlist = ''
  print("finalround")
  print(finalround)
  for i in range(finalround-2):
    a = total1[i]*12
    ii=i+1
    tourlist = tourlist + str(ii) + '回戦 全' + str(total1[i]) + '組 ' + str(race1[i]) + 'レース ' + str(passnum1[i]) + '組通過 得点上位' + str(passplus1[i]) + '組 計' + str(a) + '名\n'
  i+=1
  a = total1[i]*12
  tourlist = tourlist + '準決勝 全' +  str(total1[i]) + '組 ' +  str(race1[i]) + 'レース ' +  str(passnum1[i]) + '組通過 得点上位' +  str(passplus1[i]) + '組 計' +  str(a) + '名\n'
  i+=1
  print(i)
  print(race1)
  tourlist = tourlist + '決勝 ' +  str(race1[i]) + 'レース ' + '計12名\n'
  tournament.add_field(name=f"大会内容 形式:{keishiki}",value=tourlist, inline=False)
  await ctx3.send(embed=tournament)

  round = 1
  while round != finalround: 
    print("round start")
    passnum=passnum1[round-1]
    passplus=passplus1[round-1]
    race=race1[round-1]
    total = total1[round-1]     
    list1 = []
    list2 = []
    for i in range(1,int(total)+1):
      list1.append(i)
      list2.append(str(i))
    #print(list1)
      
    list3='組 '.join(list2) +'組'
    name= '{}回戦'.format(round)
    #print(name)
    #await ctx3.send("{}回戦 全{}組".format(round,total))
    remain = discord.Embed(title="{}回戦 全{}組".format(round,total),colour=0xe74c3c)
    remain.add_field(name="結果未提出組",value=list3, inline=True)
    now = await ctx3.send(embed=remain)

    alive = ''
    next = ''
    n=1
    remain2 = discord.Embed(title="{}回戦".format(round),colour=0xe74c3c)
    remain2.add_field(name="通過者リスト{}".format(n),value=None, inline=True)
    now2 = await ctx3.send(embed=remain2)
    
    while len(list1) != 0:
      result = await client.wait_for('message')
      if result.guild.id == ctx3.guild.id:
          #print(result.content[0:6])
          round=str(round)
          if result.content.startswith(round):
          #if res.startswith == name:
            ns=result.content[1:6] 
            num = re.sub("\\D", "", ns)
            if result.content.find('結果画像 : ') !=-1:
              if int(num) in list1:
                a = result.content.find('主催コピペ用')
                #print (a)
                #print(len(result.content))
                #print(result.content[0:6])
                #print(result.content[a+len('主催コピペ用'):])
                b = result.content[a+len('主催コピペ用'):]
                bnum = b.split('\n')
                #print("len(bnum)={}".format(len(bnum)))
                if a == -1:
                  await result.add_reaction('🤔')
                  await result.channel.send("エラー。主催コピペは正しいですか？{}".format(result.author.mention))
                elif result.content.find('結果画像 : https://') ==-1:
                  await result.add_reaction('🤔')
                  await result.channel.send("エラー。結果画像は貼られていますか？{}".format(result.author.mention))
                elif len(bnum) != int(passnum)+1: 
                  print(len(bnum))
                  print(bnum)
                  print(passnum)
                  print(round)
                  await result.add_reaction('🤔')
                  await result.channel.send("エラー。通過人数は正しいですか？{}".format(result.author.mention))
                else:
                  list1.remove(int(num))
                  #print(list1)
                  list2.remove(str(num))
                  list3='組 '.join(list2) + '組'
                  await result.add_reaction('🐟')
                  remain = discord.Embed(title="{}回戦 全{}組".format(round,total),colour=0xe74c3c)
                  remain.add_field(name="結果未提出組@{}".format(len(list1)),value=list3, inline=True)
                  await now.edit(embed=remain)

                  if len(next)+len(result.content[a+len('主催コピペ用'):]) >= 1000:
                    remain2 = discord.Embed(title=f"{round}回戦",colour=0xe74c3c)
                    remain2.add_field(name="通過者リスト{}".format(n),value=next, inline=True)
                    await ctx3.send(embed=remain2)
                    next = '' 
                    n+=1

                  alive = alive + result.content[a+len('主催コピペ用'):]
                  next = next + result.content[a+len('主催コピペ用'):]
                  #print(len(result.content[a+len('主催コピペ用'):]))
                  #print(alive)
                  #print(alive.split('\n'))
                  remain2 = discord.Embed(title=f"{round}回戦",colour=0xe74c3c)
                  remain2.add_field(name="通過者リスト{}".format(n),value=next, inline=True)
                  await now2.edit(embed=remain2)

          if result.content == 'end':
            if result.author.id == ctx3.author.id:
              if result.guild.id == ctx.guild.id:
                kessho = 1
                break

    remain = discord.Embed(title="{}回戦 全{}組 終了".format(round,total),colour=0xe74c3c)
    await now.edit(embed=remain)
    #await ctx3.send("全組集計投稿終了 {}".format(ctx3.author.mention))
    await ctx3.send("{}回戦全組集計投稿終了".format(round))

    add = ''
    if passplus != 0:
      test = await ctx3.send("{} 得点上位者を入力してください@{}".format(ctx3.author.mention,passplus))
      while passplus != 0:
        tests = await client.wait_for('message',check=check)        
        add = add + tests.content + '\n'
        alive = alive + '\n' + tests.content
        print(alive)
        passplus -= 1
        await ctx3.send("@{}".format(passplus))

    alive2 = alive.split('\n')
    alive2.remove(alive2[0])
    print("len(alive2)=")
    print(len(alive2))

    host = []
    #print(alive2)
    q=0
    #total=int(len(alive2)/12)
    #print(negroup)
    for i in range(len(alive2)):
      if alive2[i].find('★進') != -1:
        q+=1
        #print(alive2[i])
        host.append(alive2[i])
    hostlist2 = '\n'.join(host)
    aaa = str(int(round)+1)
    bbb = int(aaa)-1
    ccc = total1[bbb]
    #round = str(round)

    added = discord.Embed(title="{}回戦".format(round),colour=0xe74c3c)
    if passplus != 0:
      added.add_field(name="得点上位一覧\n",value=add, inline=False)
    if len(hostlist2) != 0:
      added.add_field(name="{}回戦進出進行役一覧(次戦{}組)\n".format(aaa,ccc),value=hostlist2, inline=False)
    else:
      added.add_field(name="{}回戦進出進行役一覧(次戦{}組)\n".format(aaa,ccc),value=None, inline=False)

    await ctx3.send(embed=added)
    

    i = 0
    check = 0
    
    await ctx3.send("{} 通過者リストに訂正がある場合は訂正を行ってください\nin 名前 フレコ: リストに追加\nout 名前 フレコ: リストから削除\nend 訂正終了".format(ctx3.author.mention))
    while check == 0:
      revise = await client.wait_for('message')
      if revise.author.id == ctx3.author.id:
        if revise.content.startswith('in'):
          alive2.append(revise.content[3:])
          i+=1
          if revise.content[3:].find('★進') != -1:
            q+=1
          await ctx3.send("added {} @{}".format(revise.content[3:],i))
        if revise.content.startswith('out'):
          if revise.content[4:] in alive2:
            alive2.remove(revise.content[4:])
            i-=1
            if revise.content[4:].find('★進') != -1:
              q-=1
            await ctx3.send("removed {} @{}".format(revise.content[4:],i))
          else:
            await ctx3.send("エラー {}が見つかりません".format(revise.content[4:]))
        if revise.content.startswith('end'):
          if q < int(ccc):
            fusoku = int(ccc)-q
            await ctx3.send("進行役が{}人不足しています".format(fusoku))
          elif i==0:
            check = 1
          else:
            await ctx3.send("エラー:全体の通過人数が正しくありません")

    host = []
    print(alive2)
    q=0
    #total=int(len(alive2)/12)
    #print(negroup)
    for i in range(len(alive2)):
      print(i)
      if q == int(ccc):
        break
      if alive2[i].find('★進') != -1:
        q+=1
        #print(alive2[i])
        host.append(alive2[i])
        alive2.remove(alive2[i])
    
    hostlist = ' '.join(host)
    round = int(round)+1
    if int(round) != finalround:
      startnext = discord.Embed(title="{}回戦終了 {}回戦開始".format(round-1,round), colour=0xe74c3c,description="@everyone {}組通過 得点上位{}名 {}レース".format(passnum1[round-1],passplus1[round-1],race1[round-1]))
    else:
      startnext = discord.Embed(title="準決勝終了 決勝戦開始", colour=0xe74c3c,description="@everyone")

    round = str(round)
    await ctx3.send(embed=startnext)

    ###組み分け###
    for i in range(1,int(ccc)+1):
      devide = []
      ramhost = random.choice(host)
      host.remove(ramhost)
      devide.append(ramhost)
      
      if keishiki == 1:
        a=11
      if keishiki == 2:
        a=5
      if keishiki == 3:
        a=3
      if keishiki == 4:
        a=2
      if keishiki == 6:
        a=1
       
      ramplayer = random.sample(alive2,a)
      #print("ramplayer")
      #print(ramplayer)
      for j in range(a):
        alive2.remove(ramplayer[j])
        devide.append(ramplayer[j])
      devidelist ='\n'.join(devide) 
      print(devidelist)
      negroup = discord.Embed(title="{}回戦{}組".format(round,i), colour=0xe74c3c)
      negroup.add_field(name="リスト",value=devidelist,inline=True)
      #nehost.add_field(''.join(host))
      #print(negroup)
      await ctx3.send(embed=negroup)

    round=int(round)
    #round += 1
    print("round end")
    print(round)

token = os.environ['DISCORD_BOT_TOKEN']
client.run(token)
