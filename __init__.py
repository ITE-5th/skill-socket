# File Path Manager
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from PIL import Image
from mycroft.util.log import LOG

# TODO: Make sure "." before module name is not missing
from code.message.image_to_text_message import ImageToTextMessage
from .code.message.close_message import CloseMessage
from .code.message.vqa_message import VqaMessage
from .code.misc.connection_helper import ConnectionHelper

LOG.warning('Running Skill Image Captioning 0')
import socket

from mycroft import MycroftSkill, intent_file_handler

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

    @intent_file_handler('caption')
    def caption(self, message):
        LOG.info('Handling ' + message)
        try:
            image = Image.open("./test.jpeg")
            LOG.info(type(image))
            msg = ImageToTextMessage(image)
            ConnectionHelper.send_pickle(self.socket, msg)
            result = ConnectionHelper.receive_pickle(self.socket)
            LOG.info(result)

        except Exception as e:
            LOG.info('Something is wrong')
            LOG.info(str(e))
            self.speak("Exception")
            self.connect()
            return False
        return True

    @intent_file_handler('vqa')
    def vqa(self, message):
        LOG.info('Handling ' + message)
        try:
            msg = VqaMessage("hello", "What?")
            ConnectionHelper.send_pickle(self.socket, msg)
        except Exception as e:
            LOG.info('Something is wrong')
            LOG.info(str(e))
            self.speak("Exception")
            self.connect()
            return False
        return True

    @intent_file_handler('close')
    def close(self, message):
        # LOG.info('Handling ' + message)
        try:
            msg = CloseMessage()
            ConnectionHelper.send_pickle(self.socket, msg)
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
