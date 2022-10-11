import requests

'''
Types class to process different types within Autocord
Types specified in autocord/types.py

message 
    <autocord.message>
channel
    <autocord.channel>
    <autocord.message.channel>
author
    <autocord.author>
    <autocord.message.author>
embed
    <autocord.embed>
    <autocord.message.embeds>
image
    <autocord.image>
    <autocord.message.attachments>
    <autocord.embeds.image>
reaction
    <autocord.reaction>
    <autocord.message.reactions>
emoji
    <autocord.emoji>
    <autocord.reaction.emoji>
'''

class message:
    def __init__(self, json):
        # create message json ect with attributes
        # check for embed or attachments
        try:
            if not json['attachments']:
                self.attachments = []
            else:
                # set attachment attributes
                self.attachments = [image(attachment) for attachment in json['attachments']]
        except KeyError:
            self.attachments = []

        # removed component support

        try:
            if not json['embeds']:
                self.embeds = []
            else:
                # create x amount of embed objects
                self.embeds = [embed(em) for em in json['embeds']]
        except KeyError:
            self.embeds = []

        self.author = author(json['author'])
        self.channel = channel(json['channel_id'])
        self.content = json['content']
        self.edited_timestamp = json['edited_timestamp']
        self.flags = json['flags']
        self.mention_everyone = json['mention_everyone']
        self.id = json['id']

        try:
            self.interaction = interaction(json['interaction'])
        except KeyError:
            self.interaction = None

        # process mentions
        self.mention_roles = [int(i) for i in json['mention_roles']]

        try:
            self.nonce = json['nonce']
        except KeyError:
            self.nonce = None

        self.pinned = json['pinned']

        # get referenced message
        try:
            request = requests.get(f'https://discord.com/api/v9/channels/{self.channel.id}/messages/{json["referenced_message"]["id"]}')
            self.referenced_message = message(request.json())
        except KeyError:
            self.referenced_message = None

        # process message reactions
        try:
            self.reactions = [reaction(re) for re in json['reactions']]
        except KeyError:
            self.reactions = []

        self.timestamp = json['timestamp']
        self.tts = json['tts']
        self.type = json['type']

        try:
            self.webhook_id = json['webhook_id']
        except KeyError:
            self.webhook_id = None


class channel:
    def __init__(self, channel):
        self.id = channel

class author:
    def __init__(self, author):
        # avatar is just discord image id
        self.avatar = author['avatar']
        self.avatar_decoration = author['avatar_decoration']
        self.descriminator = author['discriminator']
        self.id = author['id']
        self.public_flags = author['public_flags']
        self.username = author['username']

class embed:
    def __init__(self, embed):
        try:
            self.description = embed['description']
        except KeyError:
            self.description = None

        try:
            self.image = image(embed['image'])
        except KeyError:
            self.image = None

        try:
            self.title = embed['title']
        except KeyError:
            self.title = None

        try:
            self.url = embed['url']
        except KeyError:
            self.url = None

        self.color = embed['color']
        self.type = embed['type']


class image:
    def __init__(self, image):
        try:
            self.content_type = image['content_type']
        except KeyError:
            self.content_type = None

        try:
            self.filename = image['filename']
        except KeyError:
            self.filename = None

        try:
            self.id = image['id']
        except KeyError:
            self.id = None

        self.height = image['height']
        self.proxy_url = image['prox_url']
        self.url = image['url']
        self.width = image['width']
        self.size = (image['width'], image['height'])

class reaction:
    def __init__(self, reaction):
        self.count = reaction['count']
        self.emoji = emoji(reaction['emoji'])
        # indicates whether or not you reacted to the reaction
        self.me = reaction['me']

class emoji:
    def __init__(self, emoji):
        # id is none for default emojis
        self.id = emoji['id']
        self.name = emoji['name']

class interaction:
    def __init__(self, interaction):
        self.id = interaction['id']
        self.type = interaction['type']
        self.name = interaction['name']
        self.user = author(interaction['user'])
