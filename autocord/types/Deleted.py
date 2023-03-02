class Deleted:
  def __init__(self, data: dict):
    self.id: int = data['id']
    self.channel = PsuedoChannel(data['channel_id'])
    try:
      self.guild = PsuedoGuild(data['guild_id'])
    except KeyError:
      self.guild = None

class PsuedoChannel:
  def __init__(self, id):
    self.id: int = id

class PsuedoGuild:
  def __init__(self, id):
    self.id: int = id;
