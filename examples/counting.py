import autocord

# simple bot to count in a specified channel
channel = 'your counting channel'

client = autocord.client('TOKEN')
utils = autocord.utils(client)

while True:
  message = utils.FETCH_MESSAGE_HISTORY(channel, limit=1)
  try:
    count = int(message.content)+1
    client.SEND_MESSAGE(count, channel)
  except ValueError: pass
  time.sleep(20)
  
# count once every 20 seconds if the current count is a valid number
