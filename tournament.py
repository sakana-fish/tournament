import csv
import pandas as pd
import codecs
import datetime
import os
import discord
from discord.ext import commands
import asyncio
import random

intents = discord.Intents.default()
intents.members = True
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='.',intents=intents)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')  

#https://yolo.love/pandas/loc-iloc-at-iat/
#https://ja.wikipedia.org/wiki/Unicode%E3%81%AEEmoji%E3%81%AE%E4%B8%80%E8%A6%A7

###初期設定
masterid=322341906808045568 #大規模主催id
botid=703540995492675634
ch_entry=793693115386822676 #登録チャンネル
ch_bot=793692894451859456 #コマンド用チャンネル
ch_result=793693186887385138 #集計用チャンネル
ch_now=793692951201054741 #進行チャンネル
#cg_room=793493421074808902 #組み分けカテゴリー
f1='参加者リスト.csv' #参加者リスト
f2='大会設定.csv' #大会設定
f3='各回戦主催リスト.csv' #各回戦主催リスト
mode2=1 #形式(1:個人 2:タッグ 3:プルス 4:フォーマン 6:6v6)
num=int(12/mode2) #部屋の団体数

#-----------------------------------------------------
@client.command()
async def t2(ctx): #csvファイル作成
    if ctx.author.id==masterid:
        ch=client.get_channel(cg_room)
        new_role = await ctx.guild.create_role(name='1回戦1組')
        user=ctx.guild.members.get(masterid)
        print(user)
        await user.add_roles(new_role)
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),new_role: discord.PermissionOverwrite(read_messages=True)}
        await ctx.guild.create_text_channel('1回戦1組',category=ch,overwrites=overwrites)

#-----------------------------------------------------
@client.command()
async def mf(ctx): #csvファイル作成
    if ctx.author.id==masterid:
        file = open(f1, 'w')
        file = open(f2, 'w')
        file = open(f3, 'w')

#-----------------------------------------------------
@client.command()
async def clear(ctx):
    if ctx.author.id==masterid:
        await ctx.channel.purge(limit=100)

#-----------------------------------------------------
async def check(m): 
    return m.author.id == masterid


#-----------------------------------------------------
@client.command()
async def s(ctx): #大会詳細設定
    
    if ctx.author.id==masterid:
        if ctx.channel.id==ch_bot:
            id=ctx.author.id
            m=ctx.author.mention
            msg=await ctx.send('大会名を入力してください')
            msg2=await client.wait_for('message',check=check)
            title=msg2.content #形式
            await msg2.delete()
            await msg.edit(content='大会の形式を入力してください\n1:個人 2:タッグ 3:プルス 4:フォーマン 6:6v6')
            msg2=await client.wait_for('message',check=check)
            mode=int(msg2.content) #形式
            num=12/mode #組数
            await msg2.delete()
            await msg.edit(content='全回戦数を入力してください')
            msg2=await client.wait_for('message',check=check)
            round=int(msg2.content)
            await msg2.delete()
            await msg.edit(content='参加者人数を入力してください(12の倍数)')
            msg2=await client.wait_for('message',check=check)
            total=int(msg2.content) #全人数
            await msg2.delete()
            room=int(total//12) #1回戦の部屋の数
            text=f'形式:{mode} 参加者人数:{total}\n'
            text2=[]
            text2.append(['回戦数','参加組数(人数)','部屋数','通過組数(人数)','得点上位組数'])
            text2.append([0,0,0,0,0])
            for i in range(round-1):
                await msg.edit(content=f"{i+1}回戦の通過組数を入力してください(残り{total}人 {room}部屋)")
                msg2=await client.wait_for('message',check=check)
                n=int(msg2.content) #通過人数（組数）
                await msg2.delete()
                n2=int((room*n*12//num)%12) #足りない組数（得点上位）
                if n2!=0:
                    n2=12-n2
                    await msg.edit(content=f"{i+1}回戦の得点上位組数を入力してください(不足{n2}組)")
                    msg2=await client.wait_for('message',check=check)
                    n2=int(msg2.content)
                    await msg2.delete()
                if n2!=0:
                    text=text+(f"{i+1}回戦： 全{total}組 {room}部屋 {n}組通過 得点上位{n2}組\n")
                else:
                    text=text+(f"{i+1}回戦： 全{total}組 {room}部屋 {n}組通過\n")
                text2.append([i+1,total,room,n,n2])
                total=int((room*n+n2)*12//num)
                room=int(total//12)
            text=text+(f"決勝戦： 全{total}組 1部屋\n")
            text2.append([round,total,room,1,0])
            with open(f2,'w') as f: #a[数][英]
                w=csv.writer(f,lineterminator='\n')
                for i in range(len(text2)):
                    w.writerow(text2[i])
                w.writerow([0,0,0,0,0])
            await msg.delete()
            ch=client.get_channel(ch_now) 
            msg = discord.Embed(title=f"{title}",description=text)
            await ch.send(embed=msg)  

#-----------------------------------------------------
@client.command()
async def c(ctx): #登録
    #形式の判別
    def check2(m): 
        return m.author.id == ctx.author.id

    if ctx.channel.id==ch_bot:
        id=ctx.author.id
        m=ctx.author.mention
        #a=await read(f1)
        df=pd.read_csv(f1,encoding='shift-jis')
        a=df.id
        if str(id) in str(a):
            msg=await ctx.send(content=f'登録済みです {m}')
            await asyncio.sleep(3)
            await msg.delete()
        else:
            msg=await ctx.send(content=f'登録名を入力してください(★進不要) {m}')
            msg2=await client.wait_for('message',check=check2)
            name=msg2.content
            await msg2.delete()
            await msg.edit(content=f'フレンドコードを入力してください(例:1234-5678-9123) {m}')
            msg2=await client.wait_for('message',check=check2)
            fc=msg2.content
            await msg2.delete()
            await msg.edit(content=f'主催希望の方は1,希望しない方は0と入力してください {m}')
            msg2=await client.wait_for('message',check=check2)
            host=msg2.content
            await msg2.delete()
            text=f'登録名:{name}\nフレコ:{fc}'
            if host=='1':
                text=f'登録名:{name}★進\nフレコ:{fc}'
                name=name+'★進'
            await msg.edit(content=f'下記内容でよろしければ1,修正したい場合は0と入力してください {m}\n\n{text}')
            msg2=await client.wait_for('message',check=check2)
            n=msg2.content
            await msg2.delete()
            if n=='1':             
                with open(f1,'a') as f: #a[数][英]
                    w=csv.writer(f,lineterminator='\n')
                    w.writerow([0,id,name,fc,host])
                await msg.edit(content=f'登録しました {m}')
                ch = client.get_channel(ch_entry)
                text=f'{name} {fc}'
                await ch.send(text)
            else:
                await msg.edit(content=f'再度.cにて登録を行ってください {m}')
            await asyncio.sleep(3)
            await msg.delete()

#-----------------------------------------------------
@client.command()
async def d(ctx): #登録解除
    if ctx.channel.id==ch_bot:
        id=ctx.author.id
        m=ctx.author.mention
        df=pd.read_csv(f1,encoding='shift-jis')
        a=list(df.id)   
        try:
            row=a.index(id)
            df=df.drop(row)
            df.to_csv(f1,index=False,encoding='shift-jis')
            msg=await ctx.send(content=f'登録を解除しました {m}')
            await asyncio.sleep(3)
            await msg.delete()
        except ValueError:
            msg=await ctx.send(content=f'未登録です {m}')
            await asyncio.sleep(3)
            await msg.delete()

#-----------------------------------------------------
@client.command()
async def mg(ctx,n): #組み分け(make group)
    if ctx.author.id==masterid:
        if ctx.channel.id==ch_bot:
            n=int(n)
            df=pd.read_csv(f2,encoding='shift-jis')
            a=list(df.iloc[n])
            room=int(a[2])
            total=int(a[1])
            
            name=f'{n}回戦通過者.csv'
            with open(name,'w') as f:
                f.write('No,id,name,fc,host,point\n')
            name=f'{n}回戦敗者.csv'
            with open(name,'w') as f:
                f.write('No,id,name,fc,host,point\n')
            name=f'{n}回戦組み分け.csv'
            with open(name,'w') as f:
                f.write('No,id,name,fc,host\n')

            if n==1:
                df=pd.read_csv(f1,encoding='shift-jis')
                for i in range(len(df)):
                    df.No[i]=i+1
                df.to_csv(f1,index=False)
                df=df[:total]
                name=f'{n-1}回戦通過者.csv'
                df.to_csv(name,index=False)
                with open(f3,'w') as f: #a[数][英]
                    w=csv.writer(f,lineterminator='\n')
                    w.writerow(['各回戦主催id'])
            
            name=f'{n-1}回戦通過者.csv'
            df=pd.read_csv(name,encoding='shift-jis')
            df=df.sort_values('host',ascending=False)

            if len(df)==total:            
                if df.iloc[room-1][4]=='0': #主催が足りなければ
                    await ctx.send(f'主催の人数が足りません')
                else:
                    a1=list(range(0,room))
                    a2=list(range(room,total))
                    b1=random.sample(a1,room)
                    b2=random.sample(a2,total-room)

                    name=f'{n}回戦組み分け.csv'
                    #with open(name,'w') as f: #a[数][英]
                    #    w=csv.writer(f,lineterminator='\n')
                    #    w.writerow(['No','id','name','fc','host'])
                    text4=discord.Embed(title=f'{n}回戦',color=0xff0000)    
                    await ctx.send(embed=text4)
                    ch=client.get_channel(cg_room)
                    text3=[] #主催リスト
                    for i in range(room):
                        k=b1[i]
                        m=f'<@{df.iloc[k][1]}>'
                        text=f'主催:{m}\n{df.iloc[k][0]}:{df.iloc[k][2]} ({df.iloc[k][3]})\n'
                        text2=[]
                        text2.append([f'{i+1}組'])
                        text2.append(df.iloc[k])
                        text2[1][4]=n+1
                        m2=f'<@{df.iloc[k][1]}>' #メンション用
                        text3.append(df.iloc[k][1])
                        for j in range(num-1):
                            k=b2[j+(num-1)*i]
                            text=text+f'{df.iloc[k][0]}:{df.iloc[k][2]} ({df.iloc[k][3]})\n'
                            text2.append(df.iloc[k])
                            m2=m2+f'<@{df.iloc[k][1]}>'

                        with open(name,'a') as f: #a[数][英]
                            for k in range(len(text2)):
                                with open(name,'a') as f: #a[数][英]
                                    w=csv.writer(f,lineterminator='\n')
                                    w.writerow(text2[k])
                        
                        text4 = discord.Embed(title=f'{n}回戦{i+1}組',description=text)
                        msg = await ctx.send(embed=text4)
                        #chroom=await ctx.guild.create_text_channel(f'{n}回戦{i+1}組',category=ch)
                        chroom=await ctx.guild.create_text_channel(f'{n}回戦{i+1}組')
                        await chroom.send(embed=text4)
                        await chroom.send(m2)

                    df=pd.read_csv(f2,encoding='shift-jis')
                    df.iloc[0][0]=n #進行状況
                    df.to_csv(f2,index=False,encoding='shift-jis')

                    with open(f3,'a') as f: #a[数][英]
                        w=csv.writer(f,lineterminator='\n')
                        w.writerow(text3)

                    a=''
                    for i in range(room):
                        a=a+f'{i+1} ' 
                    ch=client.get_channel(ch_now)   
                    text=discord.Embed(title=f'{n}回戦進行中')
                    text.add_field(name=f'集計未提出組一覧', value=a, inline=False)                                         
                    msg = await ch.send(embed=text)
                    name='未集計組.csv'
                    a=a+f'\n{str(msg.id)}'
                    with open(name,'w') as f:                
                        f.write(a)
            else:
                n=int(total-len(df))
                await ctx.send(f'参加者リストの人数が{n}人足りません')
                            
#-----------------------------------------------------
@client.command()
async def result(ctx): #集計
    def check2(m): 
        return m.author.id == ctx.author.id

    if ctx.channel.id==ch_bot:
        df=pd.read_csv(f2,encoding='shift-jis')
        n=df.iloc[0][0] #進行状況
        with open(f3,'r') as f:
            a = f.read()
        a=a.split('\n')
        a=a[n]
        if str(ctx.author.id) in a:
            a=a.split(',')
            room=a.index(str(ctx.author.id))+1
            ok=0
            while(ok==0):
                #同部屋参加者,通過人数等読み込み
                pn=df.iloc[n][3] #通過人数(pass num)
                name=f'{n}回戦組み分け.csv'
                with open(name,'r') as f:
                    a = f.read()
                a=a.split('\n')
                room2=f'{room}組'
                room2=a.index(room2)
                for i in range(len(a)):
                    a[i]=a[i].split(',')
                mem=[] #同部屋メンバー
                for i in range(num):
                    mem.append(a[room2+i+1])
                memlist=''
                for i in range(len(mem)):
                    memlist=memlist+f'{mem[i][2]} '
                text2=f'下記順番通りに点数を入力してください(<点数>␣<点数>... 例:100 82 ... 90) {ctx.author.mention}\n{memlist}'
                text = discord.Embed(title=f'{n}回戦{room}組',description=text2)
                msg = await ctx.send(embed=text)        
                msg2=await client.wait_for('message',check=check2)
                scores=msg2.content #全人数
                await msg2.delete()      
                scores=scores.split()
                if len(scores)!=12:
                    msg3=await ctx.send('12人分の得点を正しく入力してください {ctx.author.mention}')
                    await asyncio.sleep(3)
                    await msg3.delete()
                else:
                    for i in range(len(scores)):
                        scores[i]=int(scores[i])
                    total=sum(scores)
                    a=mem
                    for i in range(len(mem)):
                        a[i].append(scores[i])

                    scores2=[] #mode2=1以外用,今回はやめておく...
                    for i in range(num): 
                        score=0
                        for j in range(mode2):
                            score=score+scores[j+i*mode2]
                        scores2.append(score)
                    
                    for i in range(len(a)):
                        a[i][0]=int(a[i][0])
                        a[i][4]=int(a[i][4])
                    a=sorted(a, reverse=False, key=lambda x: int(x[0]))
                    a=sorted(a, reverse=False, key=lambda x: int(x[4]))
                    a=sorted(a, reverse=True, key=lambda x: int(x[5]))

                    #合計点が間違っていたら警告
                    text2=f'レース後の得点の分かるツイートのurlを張り付けてください(なければ「なし」と入力してください) {ctx.author.mention}'
                    text = discord.Embed(title=f'{n}回戦{room}組',description=text2)
                    await msg.edit(embed=text)        
                    msg2=await client.wait_for('message',check=check2)
                    url=msg2.content #全人数
                    await msg2.delete()
                    memlist=''
                    for i in range(len(a)):
                        memlist=memlist+f'{a[i][0]}:{a[i][2]} ({a[i][3]}) | {a[i][5]} pts\n'  
                    text2=f'下記内容で間違いなければ1を,修正する場合は0を入力してください {ctx.author.mention}'
                    text = discord.Embed(title=f'{n}回戦{room}組',description=text2)            
                    text2=f'{memlist}\n結果画像URL:{url}'
                    text.add_field(name=f'集計結果', value=text2, inline=False) 
                    text3=''
                    for i in range(pn):
                        text3=text3+f'{a[i][0]}:{a[i][2]} ({a[i][3]})\n'
                    text.add_field(name=f'通過者', value=text3, inline=False) 
                    await msg.edit(embed=text)
                    msg2=await client.wait_for('message',check=check2)
                    ok=msg2.content
                    await msg2.delete()
                    if ok!='1':
                        ok=0
                    else:
                        ok=1
            
            #集計結果を記録   
            name=f'{n}回戦通過者.csv' 
            room2=f'{room}組'     
        
            df=pd.read_csv(name,encoding='shift-jis') #集計済みなら消す
            b=list(df.No)
            if room2 in b:
                row=b.index(room2)
                for i in range(pn+1):
                    df=df.drop(row+i)
                df.to_csv(name,index=False,encoding='shift-jis')
            name=f'{n}回戦敗者.csv' 
            df=pd.read_csv(name,encoding='shift-jis')
            b=list(df.No)
            if room2 in b:
                row=b.index(room2)
                for i in range(num-pn+1):
                    df=df.drop(row+i)   
                df.to_csv(name,index=False,encoding='shift-jis')                     
        
            name=f'{n}回戦通過者.csv' #集計結果更新
            with open(name,'a') as f: #a[数][英]
                w=csv.writer(f,lineterminator='\n')
                w.writerow([room2])
                for i in range(pn):
                    w.writerow(a[i])
            name=f'{n}回戦敗者.csv'                 
            with open(name,'a') as f: #a[数][英]
                w=csv.writer(f,lineterminator='\n')
                w.writerow([room2])
                for i in range(num-pn):
                    w.writerow(a[i+pn])
            await msg.delete()
            ch=client.get_channel(ch_result)
            text = discord.Embed(title=f'{n}回戦{room}組')            
            text2=f'{memlist}\n結果画像URL:{url}'
            text.add_field(name=f'集計結果', value=text2, inline=False) 
            text.add_field(name=f'通過者', value=text3, inline=False) 
            await ch.send(embed=text)

            name='未集計組.csv'
            with open(name,'r') as f:
                a = f.read()
            a=a.replace(f'{str(room)} ','')
            with open(name,'w') as f:
                f.write(str(a))
            a=a.split('\n')
            msgid=int(a[1])
            ch = client.get_channel(ch_now)
            msg = await ch.fetch_message(msgid)
            text=discord.Embed(title=f'{n}回戦進行中')
            text.add_field(name=f'集計未提出組一覧', value=str(a[0]), inline=False)                                         
            await msg.edit(embed=text)
            
            msg=await ctx.send(f'集計結果を記録しました. {ctx.author.mention}')
            await asyncio.sleep(3)
            await msg.delete()

        else:
            msg=await ctx.send('結果報告は主催が行ってください')
            await asyncio.sleep(3)
            await msg.delete()

#-----------------------------------------------------
@client.command()
async def cf(ctx): #得点上位等
    if ctx.author.id==masterid:
        df=pd.read_csv(f2,encoding='shift-jis')
        n=df.iloc[0][0] #進行状況
        pn=df.iloc[n][3] #通過人数(pass num)
        cb=df.iloc[n][4] #得点上位人数(pass num)
        name=f'{n}回戦通過者.csv'
        df=pd.read_csv(name,encoding='shift-jis') #集計済みなら消す
        if '組' in str(df):
            name2=f'{n}回戦通過者_before_cf.csv'
            df.to_csv(name2,index=False,encoding='shift-jis')
            for i in range(len(df)//(pn+1)):
                df=df.drop((pn+1)*i)
            df.to_csv(name,index=False,encoding='shift-jis')

            if cb!=0: #得点上位の追加
                name=f'{n}回戦敗者.csv'
                df=pd.read_csv(name,encoding='shift-jis')
                df=df.sort_values('No',ascending=True)
                df=df.sort_values('host',ascending=False)
                df=df.sort_values('point',ascending=False)
                name=f'{n}回戦通過者.csv'
                with open(name,'a') as f: #a[数][英]
                    w=csv.writer(f,lineterminator='\n')
                    for i in range(cb):
                        w.writerow(df.iloc[i])
                ch=client.get_channel(ch_result)            
                text2=''
                for i in range(pn):
                    text2=text2+f'{df.iloc[i][0]}:{df.iloc[i][2]} ({df.iloc[i][3]} | {df.iloc[i][5]} pts)\n'
                text2=text2+'----------------------------------\n'
                for i in range(5):
                    text2=text2+f'{df.iloc[pn+i][0]}:{df.iloc[pn+i][2]} ({df.iloc[pn+i][3]} | {df.iloc[pn+i][5]} pts)\n'
                text = discord.Embed(title=f'{n}回戦得点上位',description=text2) 
                await ch.send(embed=text)

                name=f'{n}回戦通過者.csv'
                df=pd.read_csv(name,encoding='shift-jis')
                df=df.sort_values('No',ascending=True)
                a=str(df.No.values)
                a=a.replace('[ ','')
                a=a.replace(']','')
                text = discord.Embed(title=f'{n}回戦通過者No',description=a) 
                await ch.send(embed=text)
 
token = os.environ['DISCORD_BOT_TOKEN2']
client.run(token)
