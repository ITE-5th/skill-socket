from .image_message import ImageMessage


class ImageToTextMessage(ImageMessage):
    def __init__(self, image):
        super().__init__(image)
