import autocord

client = autocord.Client('TOKEN')

@client.event()
async def on_ready():
  print(f"Logged in as: {client.user}")
  
@client.event()
async def on_message():
  print(f"{message.author}: {message.content}")
  
client.run()
