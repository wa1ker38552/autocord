from threading import Thread
import autocord
import requests
import time

class client:
    def __init__(self, token):
        self.token = token

        # create client session
        self.client = requests.Session()
        self.client.headers = {'authorization': self.token}

        # validate token
        request = self.client.post('https://discord.com/api/v9/channels/1/messages', json={'content': ''})
        if request.status_code == 401:
            raise autocord.TokenValidationError('Unable to validate token')

        # get metadata
        self.FETCH_METADATA()
        self.ongoing_tasks = {}

    def __enter__(self):
        return self

    def __exit__(self):
        pass

    def FETCH_METADATA(self):
        request = self.client.get('https://discord.com/api/v9/users/@me').json()

        # declare attributes
        self.bio = request['bio']
        self.discriminator = request['discriminator']
        self.email = request['email']
        self.id = request['id']
        self.phone = request['phone']
        self.username = request['username']
        self.verified = request['verified']

    def SEND_MESSAGE(self, message, channel):
        data = {'content': message}
        request = self.client.post(f'https://discord.com/api/v9/channels/{channel}/messages', json=data)

        if request.status_code == 404:
            raise autocord.NotFoundError(request.json()['message'])
        elif request.status_code == 400:
            raise autocord.BadRequestError(request.json()['message'])
        elif request.status_code == 429:
            raise autocord.UnauthorizedError(request.json()['message'])
        return request

    def END_TASK(self, id):
        # may take up to 1 second for the task to actually be deleted
        # the function checks to see if the task is deleted every second
        if str(id) in self.ongoing_tasks:
            del self.ongoing_tasks[str(id)]
        else:
            raise autocord.TaskNotFoundError('Could not found task with specified id')

    def CREATE_TASK(self, messages: dict, channel, offset=0, type=0):
        # messages should be a dictionary with the message as the key
        # and the interval as the value
        if type == 0:
            # check if function was initiated by user
            # recursively start the thread
            Thread(target=lambda: self.CREATE_TASK(messages, channel, offset, type=1)).start()
            return str(hash(channel+offset))
        else:
            # recursively started
            self.ongoing_tasks[str(hash(channel+offset))] = {
                'messages': messages,
                'channel': channel,
                'offset': offset
            }
            # kill the thread
            end = False
            time.sleep(offset)
            while True:
                # check to break out of while loop
                if end is False:
                    for message in messages:
                        # check to break out of messages loop
                        if end is False:
                            self.SEND_MESSAGE(message, channel)

                            # keep checking if thread needs to be closed
                            # check every one second
                            for i in range(messages[message]):
                                # check if task id exists within tasks list
                                if str(hash(channel+offset)) in self.ongoing_tasks:
                                    time.sleep(1)
                                else:
                                    end = True
                                    break
                        else:
                            break
                else:
                    break

    def CREATE_GROUP(self, users: list):
        # pass in user id's as strings or ints
        # add client id onto users list
        # need to add self id to create a group chat with only the two of you
        users.append(self.id)
        data = {'recipients': [str(user) for user in users]}
        request = self.client.post('https://discord.com/api/v9/users/@me/channels', json=data)

        if request.status_code == 400:
            raise autocord.BadRequestError(request.json()['message'])
        elif request.status_code == 429:
            raise autocord.UnauthorizedError(request.json()['message'])
        return request

    def LEAVE_GROUP(self, id, silent=True):
        # leave group with silent as parameter
        request = self.client.delete(f'https://discord.com/api/v9/channels/{id}?silent={str(silent).lower()}')

        if request.status_code == 404:
            raise autocord.NotFoundError(request.json()['message'])
        elif request.status_code == 400:
            raise autocord.BadRequestError(request.json()['message'])
        elif request.status_code == 429:
            raise autocord.UnauthorizedError(request.json()['message'])
        return request

    def BLOCK_USER(self, id):
        # 2 is delete
        request = self.client.put(f'https://discord.com/api/v9/users/@me/relationships/{id}', json={'type': 2})

        if request.status_code == 404:
            raise autocord.NotFoundError(request.json()['message'])
        elif request.status_code == 400:
            raise autocord.BadRequestError(request.json()['message'])
        elif request.status_code == 429:
            raise autocord.UnauthorizedError(request.json()['message'])
        return request

    def UNBLOCK_USER(self, id):
        request = self.client.delete(f'https://discord.com/api/v9/users/@me/relationships/{id}')

        if request.status_code == 404:
            raise autocord.NotFoundError(request.json()['message'])
        elif request.status_code == 400:
            raise autocord.BadRequestError(request.json()['message'])
        elif request.status_code == 429:
            raise autocord.UnauthorizedError(request.json()['message'])
        return request

    def FRIEND_REQUEST(self, id):
        request = self.client.put(f'https://discord.com/api/v9/users/@me/relationships/{id}', json={})

        if request.status_code == 404:
            raise autocord.NotFoundError(request.json()['message'])
        elif request.status_code == 400:
            raise autocord.BadRequestError(request.json()['message'])
        elif request.status_code == 429:
            raise autocord.UnauthorizedError(request.json()['message'])
        return request
