import autocord

# simple script to log deleted messages
client = autocord.Client('TOKEN')
data = {}

@client.event()
async def on_message_delete(message):
  if message.id in data:
    await client.send(message.channel.id, f"{data[message.id]['author']} deleted a message: {data[message.id]['content']}")
  else:
    await client.send(message.channel.id, "A message was deleted but it couldn't be located!")
    
@client.event()
async def on_message(message):
  data[message.id] = {
    "author": str(message.author),
    "content": message.content
  }

client.run()
