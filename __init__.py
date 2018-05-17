# File Path Manager
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import pickle

from mycroft.util.log import LOG

# TODO: Make sure "." before module name is not missing
from .message.close_message import CloseMessage
from .message.vqa_message import VqaMessage

LOG.warning('Running Skill Image Captioning 0')
import socket

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

SOCKET_PORT = 8888

LOG.warning('Running Skill Image Captioning 1')


class SocketSkill(MycroftSkill):
    def __init__(self):
        super(SocketSkill, self).__init__("ImageCaptionSkill")
        LOG.warning('Running Skill Image Captioning ')

        self.socket = None
        self.port = SOCKET_PORT
        self.host = "192.168.1.103"
        self.connect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        LOG.info('connected to server:' + self.host + ' : ' + str(self.port))

    def initialize(self):
        LOG.info("Socket Skill started")
        # self.port = IMAGE_CAPTIONING_PORT
        # self.host = self.settings["server_url"]

        LOG.info('connected to server:' + self.host + ' : ' + str(self.port))

    @intent_handler(IntentBuilder("SocketIntent").require('VQA'))
    def handle_image_caption(self, message):
        # LOG.info('Handling ' + message)
        try:
            LOG.info(str(self.socket))
            LOG.info('Sending "Hello" Message')
            msg = VqaMessage("hello", "What?")
            LOG.info(msg)  #
            LOG.info(type(msg))  #
            ConnectionHelper.send_pickle(self.socket, msg)
            LOG.info('Json Sent')

        except Exception as e:
            LOG.info('Something is wrong')
            LOG.info(str(e))
            self.speak("Exception")
            self.connect()
            return False
        return True

    @intent_handler(IntentBuilder("SocketIntent").require('Close'))
    def handle_image_caption(self, message):
        # LOG.info('Handling ' + message)
        try:
            LOG.info(str(self.socket))
            LOG.info('Sending "Hello" Message')
            msg = CloseMessage()
            LOG.info(msg)
            LOG.info(type(msg))  #
            ConnectionHelper.send_pickle(self.socket, msg)
            LOG.info('Json Sent')

        except Exception as e:
            LOG.info('Something is wrong')
            LOG.info(str(e))
            self.speak("Exception")
            self.connect()
            return False
        return True

    def stop(self):
        super(SocketSkill, self).shutdown()
        self.socket.close()
        LOG.info("Socket Skill CLOSED")


def create_skill():
    return SocketSkill()


# Connection Helper
import json

LOG.warning('Running Skill Image Captioning 2')


class ConnectionHelper:

    @staticmethod
    def send_json(socket, data):
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError) as e:
            raise Exception('You can only send JSON-serializable data')
        # send the length of the serialized data first
        socket.send('%d\n'.encode() % len(serialized))
        # send the serialized data
        socket.sendall(serialized.encode())

    @staticmethod
    def receive_json(socket):
        view = ConnectionHelper.receive(socket).decode()
        try:
            deserialized = json.loads(view)
        except (TypeError, ValueError) as e:
            raise Exception('Data received was not in JSON format')
        return deserialized

    @staticmethod
    def send_pickle(socket, object):
        try:
            serialized = pickle.dumps(object)
        except (TypeError, ValueError) as e:
            raise Exception('You can only send JSON-serializable data')
        # send the length of the serialized data first
        socket.send('%d\n'.encode() % len(serialized))
        # send the serialized data
        socket.sendall(serialized)

    @staticmethod
    def receive_pickle(socket):
        view = ConnectionHelper.receive(socket)
        try:
            deserialized = pickle.loads(view)
        except (TypeError, ValueError) as e:
            raise Exception('Data received was not in JSON format')
        return deserialized

    @staticmethod
    def receive(socket):
        # read the length of the data, letter by letter until we reach EOL
        length_str = ''
        char = socket.recv(1).decode()
        if char == '':
            return char
        while char != '\n':
            length_str += char
            char = socket.recv(1).decode()
        total = int(length_str)
        # use a memoryview to receive the data chunk by chunk efficiently
        view = memoryview(bytearray(total))
        next_offset = 0
        while total - next_offset > 0:
            recv_size = socket.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
        view = view.tobytes()
        return view
