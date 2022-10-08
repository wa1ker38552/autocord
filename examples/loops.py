import autocord

# on message function
def on_message(message):
    if message.content == 'hi':
        # change status
        client.CHANGE_STATUS(f'Last person to say hi was: {message.author.username}')
        # sendmessage
        client.SEND_MESSAGE('I changed my status!', 'CHANNEL')


# initialize client
client = autocord.client('TOKEN')
loops = autocord.loops(client)

# initialize loop
loops.CHANNEL_LISTENER('CHANNEL', on_message)
