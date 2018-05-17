# File Path Manager

from mycroft.util.log import LOG

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

        # self.socket = None
        self.port = SOCKET_PORT
        self.host = "192.168.1.103"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        LOG.info('connected to server:' + self.host + ' : ' + str(self.port))

    def initialize(self):
        LOG.info("Image Captioning Skill started")
        # self.port = IMAGE_CAPTIONING_PORT
        # self.host = self.settings["server_url"]

        LOG.info('connected to server:' + self.host + ' : ' + str(self.port))

    @intent_handler(IntentBuilder("SocketIntent").require('Socket'))
    def handle_image_caption(self, message):
        # LOG.info('Handling ' + message)
        try:
            Log.info(str(self.socket))
            LOG.info('Sending "Hello" Message')
            msg = Message()
            ConnectionHelper.send_json(self.socket, json.dumps(msg.__dict__))
            LOG.info('Json Sent')
            # self.socket.close()

        except Exception as e:
            LOG.info('Something is wrong')
            LOG.info(str(e))
            self.speak("Exception")
            return False
        return True

    def stop(self):
        super(SocketSkill, self).shutdown()
        LOG.info("Image Captioning Skill CLOSED")


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


# Message Classes


class Message(object):
    pass


class CloseMessage(Message):
    pass


class ImageMessage(Message):
    def __init__(self, image):
        self.image = image


class ImageToTextMessage(ImageMessage):
    pass


# Camera

import base64

LOG.warning('Running Skill Image Captioning 3')
import time

LOG.warning('Running Skill Image Captioning 4')
import os


class Camera:

    def __init__(self, width=800, height=600, vflip=True, hflip=True):
        self.vflip = vflip
        self.hflip = hflip
        self.resolution = (width, height)

    def take_image(self, face_count=0):
        temp_dir = FilePathManager.resolve('temp/')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        file_name = temp_dir + time.strftime("%Y%m%d-%H%M%S") + '.jpg'

        with picamera.PiCamera() as camera:
            camera.resolution = self.resolution
            camera.capture(file_name)
            camera.close()

        with open(file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        if face_count > 0:
            return encoded_string, file_name if self.check_faces(file_name=file_name, faces_count=face_count) else -1
        # with open("../Image.jpg", "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string, file_name

    def check_faces(self, file_name='./temp/Image.jpg', faces_count=1):
        import dlib
        from skimage import io
        print('analysing faces count')
        detector = dlib.get_frontal_face_detector()
        image = io.imread(file_name)
        rects = detector(image, 1)
        has_one_face = len(rects) == faces_count
        print(has_one_face)
        return has_one_face
