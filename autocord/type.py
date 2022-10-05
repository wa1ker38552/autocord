class message:
    def __init__(self, json):
        # create message json ect with attributes
        # check for embed or attachments
        if json['content'] == '':
            if not json['attachments']:
                # embed
                self.color = hex(json['embeds'][0]['color'])
                try: self.description = json['embeds'][0]['description']
                except KeyError: self.description = None
                try: self.title = json['embeds'][0]['title']
                except KeyError: self.title = None

            else:
                # attachments
                self.content_type = json['attachments'][0]['content_type']
                self.filename = json['attachments'][0]['filename']
                self.file_size = (json['attachments'][0]['height'], json['attachments'][0]['width'])
                self.url = json['attachments'][0]['url']

        else:
            # regular message
            self.content = json['content']

        self.author_id = json['author']['id']

        # message id
        self.id = json['id']
        self.timestamp = json['timestamp'].split('.')[0]
