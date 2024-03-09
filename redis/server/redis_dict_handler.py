from server import RedisHandler
import json

# from server import  server

class RedisDictHandler(RedisHandler):

    def post(self):
        body = self.request.body
        data = json.loads(body)
        deserializedMessage = self.parser.deserialize(data['message'])
        if 'set' in deserializedMessage.keys():
            key = list(deserializedMessage['set'].keys())[0]
            value = deserializedMessage['set'][key]
            self.write_to_cache(key, value)
            data_to_post = self.parser.serialize('OK')
            self.write(data_to_post)
        elif 'get' in deserializedMessage.keys():
            print(deserializedMessage)
            key = deserializedMessage['get']
            print(key)
            value = self.get_from_cache(key)
            if value is not None:
                data_to_post = self.parser.serialize(value)
                self.write(data_to_post)
            else:
                self.write(self.parser.serialize("Nil"))


