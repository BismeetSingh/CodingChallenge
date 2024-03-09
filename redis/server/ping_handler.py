import json
# from server import  RedisHandler

from server import  server

class PingHandler(server.RedisHandler):

    def post(self):
        body = self.request.body
        data = json.loads(body)
        deserializedMessage = self.parser.deserialize(data['message'])
        if deserializedMessage == 'ping':
            serializedResponse = self.parser.serialize('pong')
            self.write(serializedResponse)
