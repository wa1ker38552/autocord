# this is technically not a selfbot
# uses official discord API
import autocord

def on_message(message):
    # detect command prefix
    # detect if message author is yourself
    if message.content.startswith('!eval') and message.author.id == client.id:
        # get args by splitting string
        evaluated_expression = eval(message.content.split(' ')[0])
        client.SEND_MESSAGE(f'You evaluated expression is: {evaluated_expression}', message.channel.id)

    # simple command to end the bot
    if message.content.startswith('!end') and message.author.id == client.id:
        # since there is only one ongoing loop, it'll just delete it
        # the program should end immediately after
        for loop in loops.listeners: del loop


client = autocord.client('TOKEN')
loops = autocord.loops(client)

# run loop
loops.CHANNEL_LISTENER(CHANNEL_ID, on_message)

# autocord wasn't designed in mind of bots so some of the usage might be a might inconvenient
# also, since you're using a regular user API, the rate limits will come more often
# one good thing is you will never have to worry about intents again
