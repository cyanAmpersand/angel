class Message:
    def __init__(self,time,author,content,channel,server=None):
        self.time = time
        self.author = author
        self.content = content
        self.channel = channel
        self.server = server

