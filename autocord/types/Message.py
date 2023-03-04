from autocord.types.Embed import Embed
from autocord.types.Member import Member
from autocord.types.Deleted import PsuedoChannel
from autocord.types.Attachment import Attachment

class Message:
  def __init__(self, data: dict, client=None):
    self.__client = client
    
    self.type: int = data['type']
    self.tts: bool = data['tts']
    self.timestamp: str = data['timestamp']

    try:
      self.referenced_message: Message = Message(data['referenced_message']) if data['referenced_message'] != None else None
    except KeyError:
      self.referenced_message: Message = None
      
    self.pinned: bool = data['pinned']

    try:
      self.nonce: int = data['nonce']
    except KeyError:
      self.nonce: int = None
      
    self.mentions: list[Member] = [Member(i) for i in data['mentions']]
    self.mention_roles: list[PsuedoRole] = [PsuedoRole(i) for i in data['mention_roles']]
    self.id: int = data['id']
    self.flags: int = data['flags']
    self.embeds: list[Embed] = [Embed(i) for i in data['embeds']]
    self.edited_timestamp: str = data['edited_timestamp'] if data['edited_timestamp'] != 'None' else None
    self.content: str = data['content']
    # self.components: list[Component] -> Unsupported 
    self.channel: PsuedoChannel = PsuedoChannel(data['channel_id'])
    self.author: Member = Member(data['author'])
    self.attachments: list[Attachment] = [Attachment(i) for i in data['attachments']]
    
    try:
      self.guild_id: int = data['guild_id']
    except KeyError:
      self.guild_id: int = None

  def reply(self, content: str):
    return self.__client.send(self.channel.id, content=content, reference={'channel_id': self.channel.id, 'message_id': self.id})

  def delete(self):
    return self.__client.delete(self.channel.id, self.id)

  def edit(self, content: str):
    return self.__client.edit(self.channel.id, self.id, content)

class PsuedoMember:
  def __init__(self, data: dict):
    self.roles: list[PsuedoRole] = [PsuedoRole(i) for i in data['roles']]
    self.premium_since: str = data['premium_since'] if data['premium_since'] != 'None' else None
    self.pending: bool = data['pending']
    self.nick: str = data['nick'] if data['nick'] != 'None' else None
    self.mute: bool = data['mute']
    self.joined_at: str = data['joined_at']
    self.flags: int = data['flags']
    self.deaf: bool = data['deaf']
    self.communication_disabled_until: str = data['communication_disabled_until'] if data['communication_disabled_until'] != 'None' else None
    self.avatar: str = data['avatar'] if data['avatar'] != 'None' else None

class PsuedoRole:
  def __init__(self, id: int):
    self.id: int = id
