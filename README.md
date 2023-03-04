![autocord banner 2](https://user-images.githubusercontent.com/100868154/222307879-ca12be88-c816-47dc-8769-b8e39dbdd986.png)

**⚠️ Autocord is currently going through a complete re-write ⚠️**

_An easy to use API wrapper centered around automation_

Autocord is a Python API wrapper for Discord centered around automation. Using Autocord, you can easily automate the boring stuff using Python. Features include, sending and recieving messages, changing settings, and creating tasks. Autocord helps you easily make selfbots without the hassle of using discord.py and absolutely none of that intents bs. Syntax is pretty straightforward, quite similar to discord py.

**Installing ⚙️** <br>
Requires:
- requests > 2.28.2
- websocket > 1.5.1 `pip install websocket_client`
- asyncio (aiohttp > 3.8.3)<br>

`pip install autocord`

**Features ✨**
- Option to return data as JSON or Object
- Easy selfbot setup
- Easily customizable

**Quick Example ⚡**
```py
import autocord

client = autocord.Client('TOKEN')

@client.event
async def on_ready():
    print(f"Logged in as: {client.user}")
    
@client.event
async def on_message(message):
    if message.content == 'ping':
        message.reply('pong')
    
client.run()
```
