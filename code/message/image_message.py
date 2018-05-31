from .message import Message


class ImageMessage(Message):
    def __init__(self, image):
        super().__init__()
        self.image = image
        # self.tttt = self.__class__.__name__.encode()
        self.tttt = 1234

