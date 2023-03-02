class Member:
  def __init__(self, data: dict):
    self.username: str = data['username']
    self.public_flags: int = data['public_flags']
    self.id: int = data['id']
    self.display_name: str = data['display_name'] if data['display_name'] != 'None' else None
    self.discriminator: int = data['discriminator']
    self.avatar: str = data['avatar']

    try:
      self.avatar_decoration: str = data['avatar_decoration'] if data['avatar_decoration'] != 'None' else None
    except KeyError:
      self.avatar_decoration: str = None

  def __str__(self):
    return f'{self.username}#{self.discriminator}'
