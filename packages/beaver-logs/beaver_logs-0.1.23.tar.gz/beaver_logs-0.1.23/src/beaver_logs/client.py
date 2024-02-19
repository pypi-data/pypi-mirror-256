import socketio
import requests
import urllib3

urllib3.disable_warnings()
class Beaver:

    # TODO: Implement queueing / batching

    # TODO: put in env file?
    URL = 'https://beaver-back-production.up.railway.app'

    def __get_http_session(self):
        # TODO: skipping certificate validation
        http_session = requests.Session()
        http_session.verify = False
        return http_session

    def __init__(self, token, sio=None):
        self.token = token
        if not sio:
            self.sio = socketio.Client(http_session=self.__get_http_session())
            self.sio.connect(url=self.URL, auth={'token': token})
        else:
            self.sio = sio
        

    def make_bucket(self, bucketName):
        return Bucket(self.token, bucketName, self.sio)
    
    def log(self, bucketName, message):
        if not message:
            raise Exception('Message cannot be empty')
        
        self.sio.emit('log', {'bucket': bucketName, 'messages': [{'message': message}]})


class Bucket(Beaver):

    def __init__(self, token, bucketName, sio):
        super().__init__(token, sio=sio)
        self.bucketName = bucketName

    def log(self, message):
        super().log(self.bucketName, message)