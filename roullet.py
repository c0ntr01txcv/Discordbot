import discord
import random
from discord import app_commands
import json
from discord import Button, ButtonStyle
import copy

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'MTAzMzk4MzYzNjU4MTY2NjgxNw.GNJWKk.AxFNwhLvwhfZ8vblJrVLm3qxg0DGAU3cEWaueA'
SERVER_ID = 998193477038911588
CHANNEL_ID = 1034029270911176715
MY_GUILD = discord.Object(id=SERVER_ID)

class MyClient(discord.Client):
    def __init__(self,*,intents:discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


class RedButton(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='ゲーム',style=ButtonStyle.red)
    async def example_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Hello!', ephemeral=True)

    @discord.ui.button(label='晩飯',style=ButtonStyle.green)
    async def example_button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Hello!', ephemeral=True)
        


intent = discord.Intents.default()
intent.message_content = True
client = MyClient(intents=intent)


#キーをリストで返す
def GetKey(dict):
    list = []
    for key in dict:
        list.append(key)
    return list

#配列にidをセットして返す
def SetListId(list):
    set_list = copy.copy(list)
    id_count = 1
    for i in range (len(set_list)):
        set_list[i] = "id:" + str(id_count) + "  " + list[i] 
        id_count = id_count + 1
    return set_list
    
#入力したidとデータ内のidが一致するのか
def isMatchId(dict,key,input_id):
    flag = False
    if dict[key]["id"] == input_id:
        flag = True
    return flag

#辞書型から要素をリストとして返す
def GetElements(dict,key):
    return dict[key]["elements"]

#同じ名前のルーレットがあるか
def isSameName(keys,input_name):
    flag = False
    for key in keys:
        if(key == input_name):
            flag = True
    return flag

#ルーレットの最後のidを返す
def GetRoulletLastId(dict):
    last_key = next(iter(reversed(dict)))
    last_id = dict[last_key]["id"]
    return last_id

#辞書型のフォーマットに直す
def SetJsonFormat(dict,name):
    last_id = GetRoulletLastId(dict)
    dic_model = {
                name:{
                    "id":last_id + 1,
                    "elements":[

                    ]
                }
            }
    dict.update(dic_model)
    return dict

                
#キーを削除する                
def DeleteKey(keys,dict,input_id):
    key = keys[input_id-1]
    del dict[key]
    return dict
    

#要素のIdを割り振り直す    
def ReGiveId(dict):
    id_count = 1
    for key in dict.values():
        key["id"] = id_count
        id_count = id_count + 1
    return dict


#要素を削除する
def DeleteElement(element_id,elements):
    del elements[element_id-1]
    return elements

def isSameElement(list,element):
    flag = False
    for i in list:
        if i == element:
            flag = True
    return flag

@client.event
async def on_ready():
    print("bot起動")


  
#ルーレットの一覧を表示
@client.tree.command(
    name = "check_roulette",
    description="ルーレットを一覧表示します。",
)
async def check_roulette(inter:discord.Interaction):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)

    #キーはルーレット名
    roullets_keys = []                  
    roullets_with_id = []
    roullets_keys = GetKey(json_load)
    roullets_with_id = SetListId(roullets_keys)
    roullets_with_id = '\n'.join(roullets_with_id)

    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"現在のルーレット一覧:\n\n{roullets_with_id}")
    



#ルーレットの要素を一覧表示
@client.tree.command(
    name = "check_elements",
    description="ルーレットの要素を一覧表示します。",
)
@app_commands.describe(id="ルーレットのid")
async def check_elements(inter:discord.Interaction,id:int):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)

    roullets_keys = []
    elements = []
    elements_with_id = []

    roullets_keys = GetKey(json_load)
    selected_roullet = roullets_keys[id-1]
    elements = GetElements(json_load,selected_roullet)
    
    elements_with_id = SetListId(elements)
    elements_with_id = '\n'.join(elements_with_id)

    
    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"[{selected_roullet}]ルーレットの要素一覧:\nルーレットid:{id}\n\n{elements_with_id}")





#抽選
@client.tree.command(
    name = "spin_roulette",
    description="ルーレットをします。",
)
@app_commands.describe(id="ルーレットのid")
async def spin_roulette(inter:discord.Interaction,id:int):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)

    roullets_keys = []
    elements = []
    roullets_keys = GetKey(json_load)
    selected_roullet = roullets_keys[id-1]
    elements = GetElements(json_load,selected_roullet)


    number = random.randint(1,len(elements))
    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"[{selected_roullet}]を回した結果、[{elements[number-1]}]が出ました！")





#ルーレットの追加
@client.tree.command(
    name = "add_roullet",
    description="ルーレットを追加します。",
)
@app_commands.describe(name="ルーレット名")
async def add_roullet(inter:discord.Interaction,name:str):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)

    roullets_keys = []
    roullets_keys = GetKey(json_load)


    if(isSameName(roullets_keys,name)):
        await inter.response.defer(ephemeral=False)
        await inter.followup.send("同じ名前のルーレットがあります。")
    else:
        roullet_dict = SetJsonFormat(json_load,name)
        with open('data.json', 'w',encoding='utf-8') as f:
            json.dump(roullet_dict,f,ensure_ascii=False,indent=4)
        await inter.response.defer(ephemeral=False)
        await inter.followup.send(f"ルーレット[{name}]を作成しました。")


#ルーレットの削除
@client.tree.command(
    name = "delete_roullet",
    description="ルーレットを削除します。",
)
@app_commands.describe(id="ルーレットid")
async def delete_roullet(inter:discord.Interaction,id:int):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)

    roullet_keys = GetKey(json_load)
    roullet_key = roullet_keys[id-1]

    if isMatchId(json_load,roullet_key,id):
        result = DeleteKey(roullet_keys,json_load,id)

    gived_id_json = ReGiveId(result)

    with open('data.json', 'w',encoding='utf-8') as f:
        json.dump(gived_id_json,f,ensure_ascii=False,indent=4)

    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"ルーレット[{roullet_key}]を削除しました。")





#要素の追加
@client.tree.command(
    name = "add_element",
    description="ルーレットの要素を追加します。",
)
@app_commands.describe(id="ルーレットid",element="要素名")
async def add_element(inter:discord.Interaction,id:int,element:str):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)
    json_open.close()

    roullet_key = []
    roullet_keys = GetKey(json_load)
    roullet_last_id = GetRoulletLastId(json_load)
    if roullet_last_id > id > 0:
        roullet_key = roullet_keys[id-1]

      
    if roullet_last_id > id > 0:
        elements = []
        elements = GetElements(json_load,roullet_key)
        elements.append(element)
        if isSameElement(elements,element):
            await inter.response.defer(ephemeral=False)
            await inter.followup.send("同名の要素が存在しています。")  
            return
        
        json_load[roullet_key]["elements"] = elements
        elements_output = elements
        elements_output = SetListId(elements_output)
        elements_output = '\n'.join(elements_output)
        
        with open('data.json', 'w',encoding='utf-8') as f:
            json.dump(json_load,f,ensure_ascii=False,indent=4)

        await inter.response.defer(ephemeral=False)
        await inter.followup.send(f"ルーレット[{roullet_keys[id-1]}]に[{element}]を追加しました。\n{elements_output}")    
    else:
        await inter.response.defer(ephemeral=False)
        await inter.followup.send(f"指定したidは存在しません")

    



#要素の削除
@client.tree.command(
    name = "delete_element",
    description="ルーレットの要素を削除します。",
)
@app_commands.describe(id="ルーレットid",id2="要素id")
async def delete_element(inter:discord.Interaction,id:int,id2:int):
    json_open = open('data.json', 'r',encoding="utf-8")
    json_load = json.load(json_open)

    roullet_keys = GetKey(json_load)
    roullet_key = roullet_keys[id-1]
    
    if isMatchId(json_load,roullet_key,id):
        elements = GetElements(json_load,roullet_key)

    deleted_name = elements[id2-1]
    elements = DeleteElement(id2,elements)
        
    with open('data.json', 'w',encoding='utf-8') as f:
        json.dump(json_load,f,ensure_ascii=False,indent=4)

    elements_output = elements
    elements_output = SetListId(elements_output)
    elements_output = '\n'.join(elements_output)


    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"ルーレット[{roullet_keys[id-1]}]から[{deleted_name}]を削除しました。\n{elements_output}")
    

#サイコロ
@client.tree.command(
    name = "roll",
    description="サイコロ振ります。",
)
@app_commands.describe(number="面の数")
async def spin_roulette(inter:discord.Interaction,number:int):
    number = random.randint(1,number)
    await inter.response.defer(ephemeral=False)
    await inter.followup.send(f"{number}面のサイコロを振った結果、{number}が出ました。")


@client.tree.command(
    name = "button",
    description="テスト用"
)
async def akasata(inter:discord.Interaction):
    view = RedButton()
    await inter.response.defer(ephemeral=False)
    await inter.followup.send(view=view)
    
@discord.ui.button(label='ゲーム2',style=ButtonStyle.red)
async def example_button3(RedButton, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message('Hello!', ephemeral=True)

client.run(TOKEN)
