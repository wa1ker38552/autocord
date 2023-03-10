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
      "captcha_sitekey":"a9b5fb07-92ff-493f-86fe-352a2803b3df",
      "captcha_service":"hcaptcha",
      "captcha_rqdata":"PuiUxsKT+syvEdoNz+sOA+PS7uhT+R8gclxg0hmiRKxqldNUVgNJsSQryP90z9I6pM+iszrwWToV7ldT8AZ+emY00tuve+71u6AnVXqoNYROo62wkRudVRkdb/i6jnsb/qGu3tJNTmiFFDSEHw+rFFE5d9ouoc+xmt0LvL+O",
      "captcha_rqtoken":"Ilg0MnA3YlBCOWZxSUtZeWJ0NEt4bkN3cVNoc2JqdzFiS0hHUU91TnhqWmxCSWNzdVYvWlF1SUJlQkpDQWxCTXBmV1VGMGc9PXR1Y2w4VTVPV1VTa052dnEi.ZAtlbg.6za_LYFWd_pBS-X4Izi-MOzQ-qI"
    }
    '''
    return self.__client.send(id=self.id, content=content, attachments=attachments, reference=reference, mention=mention)
  
  def fetch_channel(self, cursor: int=None):
    return self.__client.fetch_channel(self.id, cursor)
