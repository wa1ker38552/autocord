class Embed:
  def __init__(self, data: dict):
    self.type: str = data['type']

    try:
      self.color: int = data['color']
    except KeyError:
      self.color: int = None
    
    try:
      self.description: str = data['description']
    except KeyError:
      self.description: str = None
      
    try:
      self.title: str = data['title']
    except KeyError:
      self.title: str = None

    try:
      self.image: PsuedoImage = PsuedoImage(data['image'])
    except KeyError:
      self.image: PsuedoImage = None

    try:
      self.url: str = data['url']
    except KeyError:
      self.url: str = None

    try:
      self.footer: PsuedoFooter = PsuedoFooter(data['footer'])
    except KeyError:
      self.footer: PsuedoFooter = None

class PsuedoFooter:
  def __init__(self, data: dict):
    self.text: str = data['text']

class PsuedoImage:
  def __init__(self, data: dict):
    self.height: int = data['height']
    self.width: int = data['width']
    self.proxy_url: str = data['proxy_url']
    self.url: str = data['url']
