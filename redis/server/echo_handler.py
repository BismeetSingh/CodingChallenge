import json
from server import RedisHandler
# from server import  server

class EchoHandler(RedisHandler):

    def post(self):
        body = self.request.body
        data = json.loads(body)
        deserializedNessage = self.parser.deserialize(data['message'])
        data_to_post = {"message": deserializedNessage}
        message = data_to_post['message']['echo']
        echoSerializedKey = self.parser.serialize('echo')
        data_to_post['message'] = {
            echoSerializedKey: self.parser.serialize(message)}
        self.write(data_to_post)

