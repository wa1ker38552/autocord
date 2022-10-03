from threading import Thread
import autocord
import time


class loops:
    def __init__(self, client):
        self.client = client.client
        self.autocord = client

        # create dictionary to store channels
        # that are being listened into
        self.listeners = {}

    def CHANNEL_LISTENER(self, channel, function, refresh=1, type=0):
        if type == 0:
            Thread(target=lambda: self.CHANNEL_LISTENER(channel, function, type=1)).start()
            return str(hash(channel+id(channel)))
        else:
            scanner = autocord.utils(self.autocord)
            last_scanned = scanner.FETCH_MESSAGE_HISTORY(channel, limit=1)[0]

            # add to listeners
            self.listeners[str(hash(channel+id(channel)))] = {
                'channel': channel,
                'function': function
            }

            # create variable to check if thread needs to be killed
            end = False

            while end is False:
                channel_messages = scanner.FETCH_MESSAGE_HISTORY(channel, limit=100)

                if channel_messages[0].id != last_scanned.id:
                    # loop over messages until last scanned message
                    for i, message in enumerate(channel_messages):
                        if message.id == last_scanned.id:
                            break

                    # loop over new messages
                    for x in range(i):
                        # run function specified in parameter with message object as argument
                        function(channel_messages[x])

                    # set last scanned
                    last_scanned = channel_messages[0]

                # refresh to check loop again
                for i in range(refresh):
                    if not str(hash(channel+id(channel))) in self.listeners:
                        end = True
                        break
                    time.sleep(1)

    def END(self, id):
        # end listener by killing thread
        if str(id) in self.listeners:
            del self.listeners[str(id)]
        else:
            raise autocord.ListenerNotFoundError('Could not find listener with specified id')

