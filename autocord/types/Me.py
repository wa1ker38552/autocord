class Me:
  def __init__(self, data: dict):
    for key in data:
      try:
        setattr(Me, key, int(data[key]))
      except ValueError:
        setattr(Me, key, data[key])
      except TypeError:
        setattr(Me, key, data[key])

    self.avatar_url = f'https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png'

  def __str__(self):
    return f'{self.username}#{self.discriminator}'
