class message:
    def __init__(self, json):
        # create message json ect with attributes
        print(json)
        self.content = json['content']
        self.author_id = json['author']['id']

        # message id
        self.id = json['id']
        self.timestamp = json['timestamp'].split('.')[0]