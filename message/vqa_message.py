from .message import Message


class VqaMessage(Message):
    def __init__(self, image, question):
        super().__init__(image)
        self.question = question
