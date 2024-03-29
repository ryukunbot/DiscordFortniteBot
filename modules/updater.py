import nextcord
import json
import os
import requests
from replit import db
from colorama import Fore

def updater():
  print(Fore.GREEN + "アップデートを確認中です..." + Fore.RESET)  
  with open('config.json','r') as f:
    config = json.load(f)
  with open('bots.json','r') as f:
    bots = json.load(f)

  version = bots['version']  
  git = f"{bots['git_raw']}/{bots['git_branch']}"
  new_version = requests.get(f"{git}/bots.json").json()['version']
  if version != new_version:
    print(Fore.GREEN + f"バージョン{new_version}へのアップデートを確認しました\nアップデートを実行します" + Fore.RESET)
    new_files = requests.get(f"{git}/files.json").json()
    with open('files.json','w',encoding='utf-8') as f:
      json.dump(new_files,f,indent=2,ensure_ascii=False)
    with open('files.json','r') as f:
      files = json.load(f)['files']   
    for file in files:
      new_file = requests.get(f"{git}/{file}").text
      with open(f'{file}','w') as f:
        f.write(new_file)
    new_main = requests.get(f"{git}/main.py").text 
    with open('main.py','w') as f:
      f.write(new_main)
    new_config = requests.get(f"{git}/config.json").json()
    for key in config:
      db[key] = str(config[key])
    with open('config.json','w',encoding='utf-8') as f:
      json.dump(new_config,f,indent=2,ensure_ascii=False)
    for key in db.keys():
      with open('config.json','r') as f:
        config = json.load(f)
        config[key] = str(db[key])
        del db[key]
      with open('config.json','w',encoding='utf-8') as f:
        json.dump(config,f,indent=2,ensure_ascii=False)
    with open('bots.json','r') as f:     
      bots = json.load(f)
      bots['version'] = new_version
    with open('bots.json','w',encoding='utf-8') as f:
      json.dump(bots,f,indent=2,ensure_ascii=False)    
    print(Fore.GREEN + f"バージョン{new_version}へのアップデートが正常に完了しました" + Fore.RESET)
  else:
    print(Fore.GREEN + "アップデートは見つかりませんでした" + Fore.RESET)

def command_check_update():
  with open('config.json','r') as f:
    config = json.load(f)
  with open('bots.json','r') as f:
    bots = json.load(f)

  version = bots['version']  
  git = f"{bots['git_raw']}/{bots['git_branch']}"
  new_version = requests.get(f"{git}/bots.json").json()['version']
  color = nextcord.Colour(int(config['color'],16))  
  if version != new_version:
    embed=nextcord.Embed(title="アップデートを確認しました",description=f"{new_version}へのアップデートを確認しました\n適応する場合再起動してください",color=color)
  else:
    embed=nextcord.Embed(title="アップデートは見つかりませんでした",description=f"アップデートは見つかりませんでした\n現在のバージョン{version}は最新です",color=color)
  return embed
