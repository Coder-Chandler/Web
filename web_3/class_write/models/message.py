from models import Model


# 定义一个 class 用于保存 message
# Model中的__repr__ -> {'message': 'hello', 'author': 'gua'} --> < Message author: (gua) message: (hello) >
class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')
