## Install

```
sudo apt update
sudo apt install git python3-pip -y
```

```
git clone https://github.com/AliAshgar/Taiko.git
cd Taiko
```

```
pip install web3
```

```
pip install pytz
```

```
pip install colorama
```

```
pip install python-telegram-bot
```

```
pip install prompt_toolkit
```

Edit config.json untuk penyesuaian bot telegram
```
cd utils
```
```
nano config.json
```

```
{
    "taiko_url": "https://rpc.taiko.xyz",
    "chat_id": "CHAT ID",
    "auth_token": "TOKEN BOT",
    "bot_notif": false,
    "run_time": "" 
}
```

save (CTRL+X Y enter)

```
cd ..
```

 Run bot
```
python3 run.py
```
 

