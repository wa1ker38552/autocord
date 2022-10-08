<p align="center">
<img src="https://user-images.githubusercontent.com/100868154/194678409-60841a51-f066-4aa0-817f-670f7d3b8b4c.png" width=1050; height=225;></img>
</p>


_An easy to use API wrapper centered around automation_

Autocord is a Python API wrapper for Discord centered around automation. Using Autocord, you can easily send messages, create tasks, and much more. The purpose of Autocord is to provide users with less hassle when using requests.

**Installing**
<br>
Requires `python>3.7`
<br>
`pip install autocord`

**Quick Example**
```py
# inialize autocord client
client = autocord.client('TOKEN')

# send the message 'hi'
client.SEND_MESSAGE('Hi', CHANNEL_ID)

# create a task that sends the message 'hi' every 5 seconds
id = client.CREATE_TASK({'Hi', 5}, CHANNEL_ID)
print(client.ongoing_tasks)

# end the task
client.END_TASK(id)
```

# Client
**Getting Started**
<br>
To get started, initialize a client. The client is essentially a `request.Session()` object with included parameters. Also on initialization, client feches basic metadata to show your id, username, discriminator, and more. 
```py
with autocord.client('TOKEN') as client:
    print(client.id)

# or...
    
client = autocord.client('TOKEN')
print(client.id)
```

**Creating Tasks**
<br>
You can easily create a task using Autocord using the `self.CREATE_TASK(messages, channel)` function. The messages parameter is a dictionary with message as the key and the interval as the value. 
```py
data = {
    # send hi and wait 5 seconds
    'hi': 5,
    # send bye and wait 5 seconds
    'bye': 5
}
client.CREATE_TASK(data, CHANNEL_ID)
```
Additionally, you can also specify an offset parameter to wait a certain amount of time before starting the thread.
```py
# start thread 10 seconds after being run
client.CREATE_TASK(data, CHANNEL_ID, offset=10)
```
Ending a task is quite simple. Once a task is created, it is added to `self.ongoing_tasks` and also returns the task id. You can call the attribute `ongoing_tasks` or take a value from the `CREATE_TASK` function to find your task id. To end a task, just call `self.ENDTASK(id)`
```py
id = client.CREATE_TASK(messages, CHANNEL_ID)
client.END_TASK(id)

# or...

client.CREATE_TASK(messages, CHANNEL_ID)
for task in client.ongoing_tasks:
    client.END_TASK(task)
```
**Creating Groups**
<br>
You can also create discord groups using `self.CREATE_GROUP(users)`. `CREATE_GROUP` takes in a list of user id's as a paramter. Creating a group with return a `request.response` object.
```py
# create a group with user id's 000000 and 111111
client.CREATE_GROUP([000000, 111111])

# getting a response
response = client.CREATE_GROUP([])
print(response.json())
```
**Interacting With Users**
<br>
You can interact with other users by sending them a friend request, blocking them, and unblocking them.
```py
# all of these methods return request.response objects

# send a friend request to specified user id
client.FRIEND_REQUEST(id)

# block user with specified id
client.BLOCK(id)

# unblock user with specified id
client.UNBLOCK(id)
```

**Managing Your Account**
<br>
Using autocord, you can also manage your account settings such as changing your status, bio, and username. Changing your status, bio, or username is repeatedly is not recommended though, it could get you banned.
```py
# all of these methods return request.response objects

# change your status
client.CHANGE_STATUS(message='This is a new status!')
# change your status emoji
client.CHANGE_STATUS(emoji='')
# changing both
client.CHANGE_STATUS(message='This is a status with an emoji', emoji='')

# change your bio
client.CHANGE_BIO(message='This is a new bio!')
# change your bio accent color
# takes in a hex or int value as a parameter
client.CHANGE_STATUS(color=0xffffff)
# changing both
client.CHANGE_STATUS(message='This is a bio with color', color=0xffffff)

# change your username
client.CHANGE_USERNAME('MyNewUsername', 'YOUR PASSWORD')
```

# Utils
You can use `autocord.utils` to preform miscallaneous tasks. To create a util object, initialize it using:
```py
client = autocord.client('TOKEN')
util = autocord.utils(client)
```
`autocord.util` takes in an `autocord.client` object as a parameter.

**Fetching Channel History**
<br>
You can fetch message history from a channel by calling `self.FETCH_MESSAGE_HISTORY(CHANNEL_ID)`. By default, it will fetch 100 messages although you can specify that by changing the limit parameter.
```py
util = autocord.utils(client)

# fetch 100 most recent messages
util.FETCH_MESSAGE_HISTORY(CHANNEL_ID)

# fetch 1000 most recent messages
util.FETCH_MESSAGE_HISTORY(CHANNEL_ID, limit=1000)
```
By default, `FETCH_MESSAGE_HISTORY` will wait until it isn't rate limited if discord rate limits you. You can break out of the loop by setting the retry parameter to False.
```py
# try fetching 10,000 messages
# util will wait if it gets rate limited
util.FETCH_MESSAGE_HISTORY(CHANNEL_ID, limit=10000)

# try fetching 10,000 messages
# util will return if it gets rate limited
util.FETCH_MESSAGE_HISTORY(CHANNEL_ID, limit=10000, retry=False)
```

# Loops
You can use `autocord.loops` to set up loops centered around your discord account. To create a loop, you have to initialize it by passing in `autocord.client` as a parameter.
```py
client = autocord.client('TOKEN')
loops = autocord.loops(client)
```
`autocord.loops` takes in `autocord.client` as a parameter.
**Listening to Channel**
<br>
Using a loop, you can listen to a channel for messages as such:
```py
def my_function(message):
    print(message.content)

loops.CHANNEL_LISTENER(CHANNEL_ID, my_function)
```
`loops.CHANNEL_LISTENER()` takes in two required parameters, channel id, and function. The channel id is the channel that you're listening into and the function is the function that the loop calls when it recieves a new message. `loops.CHANNEL_LISTENER` takes in an optional parameters as well.
```py
def on_message(message):
    client.SEND_MESSAGE(f'Message recieved: {message.content}', message.channel.id)
    
# creates a regular loop object
loops.CHANNEL_LISTENER(CHANNEL_ID, on_message)

# set refresh limit for a loop
# refresh the channel every 60 seconds
loops.CHANNEL_LISTENER(CHANNEL_ID, on_message, refresh=60)
```
Note that the `CHANNEL_LISTENER` function will loop every `refresh` seconds and check for new messages. Once it finds a new message, it will immediately run the function that was specified as a parameter. Hence, if you recieved 30 messages while the loop was still waiting `refresh` seconds, it will activate the function 30 times almost simultaniously.
<br><br>
Upon running the function specified in the parameters, the loop will run a function and pass in a `autocord.message` object as a parameter. 

**Auto Response**
<br>
Additionally, `autocord.loops` can automatically return a response while running a loop. This can be done using `loops.AUTO_REPLY()`. Auto reply takes in three required parameters. These include, channel, indicator, and response. The channel is the channel that you're listening into. The indicator is the keyword that you're looking for in an message, and the response is the response that you give to the message.
```py
# automatically response to any message with 'hi' in it with 'Hi there!' on CHANNEL_ID
loops.AUTO_REPLY(CHANNEL_ID, 'hi', 'Hi there!')
```
You can also specify a `include_self` parameter to specify whether or not you want to respond to your own messages.
```py
loops.AUTO_REPLY(CHANNEL_ID, '!ping', 'pong', include_self=True)
```
**Ending a Loop**
<br>
All loop functions return an id which you can use to end a loop's thread. You can also call `self.listeners` to locate any running loops.
```py
loops = autocord.loops(client)

# run a loop for 2 hours
id = loops.CHANNEL_LISTENER(CHANNEL_ID, on_message)
time.sleep(7200)
loops.END(id)
```
