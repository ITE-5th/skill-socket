# File Path Manager
# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import os
import socket

import cv2
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import LOG

from .code.message.close_message import CloseMessage
# TODO: Make sure "." before module name is not missing
from .code.message.image_to_text_message import ImageToTextMessage
from .code.message.vqa_message import VqaMessage
from .code.misc.connection_helper import ConnectionHelper

SOCKET_PORT = 8888

LOG.warning('Running Skill Image Captioning 0')


class SocketSkill(MycroftSkill):
    def __init__(self):
        super(SocketSkill, self).__init__("Socket Skill")
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

    @staticmethod
    def take_image():
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        del camera
        return image

    @staticmethod
    def load_image(relative_path):
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        abs_file_path = os.path.join(script_dir, relative_path)
        image = cv2.imread(abs_file_path)
        return image

    @intent_file_handler('caption.intent')
    def caption(self, message):
        # LOG.info('Handling ' + message)
        try:
            image = self.take_image()
            LOG.info(type(image))
            msg = ImageToTextMessage(image.tolist())
            ConnectionHelper.send_json(self.socket, msg)
            # result = ConnectionHelper.receive_json(self.socket)
            # LOG.info(result)

        except Exception as e:
            LOG.info('Something is wrong')
            LOG.info(str(e))
            self.speak("Exception")
            self.connect()
            return False
        return True
    #
    # @intent_file_handler('vqa.intent')
    # def vqa(self, message):
    #     # LOG.info('Handling ' + message)
    #     try:
    #         msg = VqaMessage("hello", "What?")
    #         ConnectionHelper.send_pickle(self.socket, msg)
    #         result = ConnectionHelper.receive_json(self.socket)
    #         LOG.info(result)
    #     except Exception as e:
    #         LOG.info('Something is wrong')
    #         LOG.info(str(e))
    #         self.speak("Exception")
    #         self.connect()
    #         return False
    #     return True

    @intent_file_handler('close.intent')
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
