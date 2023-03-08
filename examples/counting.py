import autocord

client = autocord.Client('TOKEN')
CHANNEL = 0000000000000000000

@client.event
async def on_ready():
   print(f'Logged in as: {client.user}')
    
@client.event
async def on_message(message):
  global CHANNEL
  if message.channel.id == CHANNEL:
    try:
      await client.send(message.channel.id, int(message.content)+1)
    except ValueError:
      pass

    
client.run()
