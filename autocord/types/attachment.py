class Attachment:
  def __init__(self, data: dict):
    self.url: str = data['url']
    self.size: int = data['size']
    self.proxy_url: str = data['proxy_url']
    self.id: int = data['id']
    self.filename: str = data['filename']
    self.content_type: str = data['content_type']

    try:
      self.width: int = data['width']
      self.height: int = data['height']
    except KeyError:
      self.width: int = None
      self.height: int = None
