# Autocord

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
# Utils
You can use autocord.utils to preform miscallaneous tasks. To create a util object, initialize it using:
```py
client = autocord.client('TOKEN')
util = autocord.utils(client)
```
autocord.util takes in a client object as a parameter.

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
