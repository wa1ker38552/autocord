import json
import time
import asyncio
import requests
import websocket
from autocord import op
from autocord import errors
from threading import Thread
from autocord.types.Me import Me
from autocord.types.Message import Message
from autocord.types.Deleted import Deleted

class Client:
  def __init__(self, token, return_type='object'):
    self.client = requests.Session()
    self.client.headers = {'Authorization': token}
    try:
      data = self.client.get('https://discord.com/api/v9/users/@me')
      try:
        data = data.json()
        data['message']
        raise errors.UnauthorizedError(data['message'])
      except KeyError:
        self.token = token
        self.user = Me(data)

        self.on_ready = []
        self.on_message = []
        self.on_message_delete = []
        self.on_message_update = []

        self.return_type = return_type if return_type in ['object', 'json'] else 'object'
        self.ws_url = 'wss://gateway.discord.gg/?v=9&encoding=json'
        self.auth = {
          "token": self.token,
          "properties": {
              "$os": "windows",
              "$browser": "chrome",
              "$device": "pc"
          }
        }
    
    except requests.exceptions.JSONDecodeError:
      raise errors.TooManyRequests(data.text.strip())

  def event(self, func):
    if func.__name__ == 'on_ready':
      self.on_ready.append(func)
    elif func.__name__ == 'on_message':
      self.on_message.append(func)
    elif func.__name__ == 'on_message_delete':
      self.on_message_delete.append(func)
    elif func.__name__ == 'on_message_update':
      self.on_message_update.append(func)

  def send_ws(self, event, payload):
    self.ws.send(json.dumps({"op": event, "d": payload}))

  def recieve_messages(self):
    while True:
      data = json.loads(self.ws.recv())
      if data["op"] == op.DISPATCH:     
        if data['t'] == 'MESSAGE_DELETE':
          if self.return_type == 'json': data = data['d']
          else: data = Deleted(data['d'])
          for func in self.on_message_delete:
            asyncio.run(func(data))

        elif data['t'] == 'MESSAGE_UPDATE':
          if self.return_type == 'json': data = data['d']
          else: data = Message(data['d'], self)
          for func in self.on_message_update:
            asyncio.run(func(data))
        
        elif data["t"] == "MESSAGE_CREATE":
          if self.return_type == 'json': data = data['d']
          else: data = Message(data['d'], self)
          for func in self.on_message:
            asyncio.run(func(data))

  def send_heartbeat(self):
    while self.hb_interval is not None:
      self.send_ws(op.HEARTBEAT, self.auth)
      time.sleep(self.hb_interval)

  def connect(self):
    self.ws = websocket.WebSocket()
    self.ws.connect(self.ws_url)
    self.send_ws(op.IDENTIFY, self.auth)
    response = json.loads(self.ws.recv())

    if response['op'] != 10:
      raise errors.UnexpectedSocketResponse('Try running the application again')
    else:
      self.hb_interval = (response["d"]["heartbeat_interval"]-2000)/1000
      Thread(target=self.send_heartbeat).start()
      Thread(target=self.recieve_messages).start()

  # Client functions
  async def send(self, id: int, content: str=None, attachments: list=None, reference: dict=None) -> Message:
    payload = {'content': content}
    if reference:
      payload['message_reference'] = reference
      
    data = self.client.post(
      f'https://discord.com/api/v9/channels/{id}/messages',
      json=payload
    )
    data = data.json()
    try:
      data['errors']
      if 'channel_id' in data['errors']:
        raise errors.InvalidFormBody(data['errors']['channel_id']['_errors'][0]['message'])
      elif 'content' in data['errors']:
        raise errors.InvalidFormBody(data['errors']['content']['_errors'][0]['message'])
      else:
        raise errors.InvalidFormBody(data['message'])
    except KeyError:
      try:
        raise errors.InvalidFormBody(data['message'])
      except KeyError:
        if self.return_type == 'object':
          return Message(data, self)
        else:
          return data

  async def delete(self, id: int, message: int):
    data = self.client.delete(f'https://discord.com/api/v9/channels/{id}/messages/{message}')
    try:
      data = data.json()
      try:
        raise errors.InvalidFormBody(data['errors']['message_id']['_errors'][0]['message'])
      except KeyError:
        try:
          raise errors.InvalidFormBody(data['errors']['channel']['_errors'][0]['message'])
        except KeyError:
          raise errors.InvalidFormBody(data['message'])
    except requests.exceptions.JSONDecodeError: pass

  async def edit(self, id: int, message: int, content: str):
    data = self.client.patch(f'https://discord.com/api/v9/channels/{id}/messages/{message}', {'content': content})
    data = data.json()
    try:
      raise errors.InvalidFormBody(data['errors']['message_id']['_errors'][0]['message'])
    except KeyError:
      try:
        raise errors.InvalidFormBody(data['errors']['channel']['_errors'][0]['message'])
      except KeyError:
        try:
          raise errors.InvalidFormBody(data['message'])
        except KeyError:
          if self.return_type == 'object':
            return Message(data, self)
          else:
            return data
        

  async def fetch_channel(self, id: int, cursor: int=None) -> Message:
    if cursor is None:
      data = self.client.get(f'https://discord.com/api/v9/channels/{id}/messages')
    else:
      data = self.client.get(f'https://discord.com/api/v9/channels/{id}/messages?before={cursor}')
    try:
      data = data.json()
      try:
        raise errors.InvalidFormBody(data['channel_id']['_errors'][0]['message'])
      except KeyError:
        raise errors.InvalidFormBody(data['message'])
    except ValueError: pass
    except TypeError: pass

    if self.return_type == 'object':
      return [Message(i, self) for i in data]
    else:
      return data
  
  def run(self):
    self.connect()
    for func in self.on_ready:
      asyncio.run(func())
