import requests
import autocord
import math
import time


def query_messages(raw):
    # for turning json into <message object>
    messages = []
    for item in raw:
        # append message object
        messages.append(autocord.message(item))
    return messages

class utils:
    def __init__(self, client):
        # pass in autocord.client as parameter
        self.client = client.client
        self.autocord = client

    def FETCH_MESSAGE_HISTORY(self, channel, limit=100):
        messages = []
        # request message history

        if limit > 100:
            request = self.client.get(f'https://discord.com/api/v9/channels/{channel}/messages?limit=100')
        else:
            # fetch leftover amount
            request = self.client.get(f'https://discord.com/api/v9/channels/{channel}/messages?limit={limit % 100}')

        # turn json into <message object>
        messages.extend(query_messages(request.json()))

        if not limit > 100:
            # return messages if already finished checking limit
            return messages
        else:
            for i in range(math.floor(limit / 100) - 1):
                last_message = messages[len(messages) - 1].id
                request = self.client.get(f'https://discord.com/api/v9/channels/{channel}/messages?limit=100&before={last_message}')

                try:
                    # rate limit, retry after
                    if request.json()['message'] == 'The resource is being rate limited.':
                        time.sleep(request.json()['retry_after'])
                        request = self.client.get(f'https://discord.com/api/v9/channels/{channel}/messages?limit=100&before={last_message}')

                except TypeError:
                    pass

                # append new data
                messages.extend(query_messages(request.json()))

            # return data
            return messages
