from autocord.types.Member import Member

class DmChannel:
  def __init__(self, data: dict, client=None):
    self.__client = client
    
    self.id: int = data['id']
    self.type: int = data['type']
    self.last_mesasge_id: int = data['last_message_id']
    self.flags: int = data['flags']
    self.recipients: list[Member] = [Member(i) for i in data['recipients']]

  def send(self, content: str=None, attachments: list=None, reference: dict=None, mention: bool=True):
    # depricated due to captcha
    '''
    {
      "captcha_key":[
        "captcha-required"
      ],
      "captcha_sitekey": "x",
      "captcha_service": "hcaptcha",
      "captcha_rqdata": "x",
      "captcha_rqtoken": "x"
    }
    '''
    return self.__client.send(id=self.id, content=content, attachments=attachments, reference=reference, mention=mention)
  
  def fetch_channel(self, cursor: int=None):
    return self.__client.fetch_channel(self.id, cursor)
