from dis import dis
from pickle import FALSE
from re import I
import discord
import random
from pprint import pformat
from discord import app_commands
from discord.ext import commands
import json
from discord import Button, ButtonStyle

# 自分のBotのアクセストークン
TOKEN = 
SERVER_ID = 
CHANNEL_ID = 
MY_GUILD = discord.Object(id=SERVER_ID)

class MyClient(discord.Client):
    def __init__(self,*,intents:discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)




intent = discord.Intents.default()
intent.message_content = True
client = MyClient(intents=intent)



elements = []
roullets = []
last_id = 0

@client.event
async def on_ready():
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)

    #最上位キーの取り出し
    for key in json_load:
        roullets.append(key)


  
#ルーレットの一覧を表示
@client.tree.command(
    name = "check_roulette",
    description="ルーレットを一覧表示します。",
)
async def check_roulette(inter:discord.Interaction):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    roullets_list = []
    i=1
    for key in json_load:
        roullets_list.append("id:"+ str(i) +"  " + key)
        i = i + 1
    roullets_list = '\n'.join(roullets_list)

    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"現在のルーレット一覧:\n\n{roullets_list}")
    

#ルーレットの要素の一覧を表示
@client.tree.command(
    name = "check_elements",
    description="ルーレットの要素を一覧表示します。",
)
@app_commands.describe(id="ルーレットのid")
async def check_roulette(inter:discord.Interaction,id:int):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    roullet_names = []
    



    for name in json_load:
        roullet_names.append(name)

    name = roullet_names[id-1]
    i = 1
    list = []
    elements = []
    
    for key in json_load.values():
        if key["id"] == id:
            list=json_load[roullet_names[id-1]]["elements"]
            print(list)
            for m in list:
                elements.append("id:" + str(i) + "  "+ m)
                i = i + 1 
    elements = '\n'.join(elements)

    

    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"[{name}]のルーレット一覧:\n\n{elements}")



#抽選
@client.tree.command(
    name = "spin_roulette",
    description="ルーレットをします。",
)
@app_commands.describe(id="ルーレットのid")
async def spin_roulette(inter:discord.Interaction,id:int):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    roullet_names = []
    for name in json_load:
        roullet_names.append(name)
    
    for key in json_load.values():
        if key["id"] == id:
            elements=json_load[roullet_names[id-1]]["elements"]


    number = random.randint(1,len(elements))
    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"[{roullet_names[id-1]}]を回した結果、[{elements[number-1]}]が出ました！")


#ルーレットの追加
@client.tree.command(
    name = "add_roullet",
    description="ルーレットを追加します。",
)
@app_commands.describe(name="ルーレット名")
async def add_roullet(inter:discord.Interaction,name:str):
    
    #最後尾のid取り出し
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    roullet_names = []
    for roullet_name in json_load:
        roullet_names.append(roullet_name)
    for i in roullet_names:
        if(i == name):
            if name != i:
                last_key = next(iter(reversed(json_load)))
                last_id = json_load[last_key]["id"]

                dic = {
                    name:{
                        "id":last_id + 1,
                        "elements":[

                        ]
                    }
                }
                with open('data.json', 'r',encoding='utf-8') as f:
                    roulletsjson = json.load(f)
                roulletsjson.update(dic)

                with open('data.json', 'w',encoding='utf-8') as f:
                    json.dump(roulletsjson,f,ensure_ascii=False,indent=4)
                
                await inter.response.defer(ephemeral=False)
                await inter.followup.send(f"ルーレット[{name}]を作成しました。")
            else:
                await inter.response.defer(ephemeral=False)
                await inter.followup.send("同じ名前のルーレットがあります。")

    

#ルーレットの削除
@client.tree.command(
    name = "delete_roullet",
    description="ルーレットを削除します。",
)
@app_commands.describe(id="ルーレットid")
async def add_roullet(inter:discord.Interaction,id:int):

    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)

    roullet_names = []
    roullet_name = ""
    for name in json_load:
        roullet_names.append(name)
    
    for key in json_load.values():
        if key["id"] == id:
            roullet_name = roullet_names[id-1]
    del json_load[roullet_name]
    del roullet_names[id-1]
    i = 1
    for key in json_load.values():
        key["id"] = i
        i = i + 1

    with open('data.json', 'w',encoding='utf-8') as f:
        json.dump(json_load,f,ensure_ascii=False,indent=4)

    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"ルーレット[{roullet_name}]を削除しました。")





   


#要素の追加
@client.tree.command(
    name = "add_element",
    description="ルーレットの要素を追加します。",
)
@app_commands.describe(id="ルーレットid",element="要素名")#ルーレットの選択をさせたい
async def add_element(inter:discord.Interaction,id:int,element:str):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    roullet_names = []
    for name in json_load:
        roullet_names.append(name)
    
    for key in json_load.values():
        if key["id"] == id:
            elements=json_load[roullet_names[id-1]]["elements"]

    elements.append(element)
    with open('data.json', 'w',encoding='utf-8') as f:
        json.dump(json_load,f,ensure_ascii=False,indent=4)

    elements = '\n'.join(elements)
    
    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"ルーレット[{roullet_names[id-1]}]に[{element}]を追加しました。")



#要素の削除
@client.tree.command(
    name = "delete_element",
    description="ルーレットの要素を削除します。",
)
@app_commands.describe(id="ルーレットid",id2="要素id")
async def delete_element(inter:discord.Interaction,id:int,id2:int):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    roullet_names = []
    for name in json_load:
        roullet_names.append(name)
    
    for key in json_load.values():
        if key["id"] == id:
            elements=json_load[roullet_names[id-1]]["elements"]

    deleted_name = elements[id2-1]
    del elements[id2-1]
    print(elements)
    with open('data.json', 'w',encoding='utf-8') as f:
        json.dump(json_load,f,ensure_ascii=False,indent=4)


    list = pformat(elements)
    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"ルーレット[{roullet_names[id-1]}]から[{deleted_name}]を削除しました。")
    

#サイコロ
@client.tree.command(
    name = "roll",
    description="サイコロ振ります。",
)
@app_commands.describe(arg="面の数")
async def spin_roulette(inter:discord.Interaction,arg:int):
    number = random.randint(1,arg)
    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"{arg}面のサイコロを振った結果、{number}が出ました。")


client.run(TOKEN)
