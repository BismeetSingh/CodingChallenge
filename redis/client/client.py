import tornado.httpclient
import json
import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from parsers.resp_parser import RespParser

from parsers.resp_parser import RespParser


class TornadoHttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.http_client = tornado.httpclient.AsyncHTTPClient()
        self.parser = RespParser()

    def close(self):
        self.http_client.close()

    def _build_url(self, path, params=None):
        # serializedPath = self.parser.serialize(path)
        url = f"{self.base_url}/{path}"
        print(url)
        if params:
            url += "?" + "&".join([f"{key}={value}" for key, value in params.items()])
        return url

    async def get(self, path, params=None):
        url = self._build_url(path, params)
        print(url)
        response = await self.http_client.fetch(url)
        return response.body.decode("utf-8")

    async def fetchResponse(self, body):
        response = await self.http_client.fetch(self.url, method="POST", headers=self.headers, body=body)
        decodedResponse = response.body.decode('utf-8')
        return decodedResponse

    async def post(self, path, data=None):

        self.url = self._build_url(path)
        self.headers = {"Content-Type": "application/json"}

        if data['message'] == 'ping':
            data['message'] = self.parser.serialize(data['message'])
            body = json.dumps(data)
            decodedResponse = await self.fetchResponse(body)
            deserializedResponse = self.parser.deserialize(decodedResponse)
            return deserializedResponse

        elif "echo" in data['message']:
            data['message']['echo'] = self.parser.serialize(data['message']['echo'])
            data['message'] = {self.parser.serialize('echo'): data['message']['echo']}
            body = json.dumps(data)
            decodedResponse = await self.fetchResponse(body)
            decodedResponse = json.loads(decodedResponse)
            print(decodedResponse)
            deserializedResponse = self.parser.deserialize(decodedResponse['message'])
            return deserializedResponse

        elif 'set' in data['message']:

            key = list(data['message']['set'].keys())[0]
            data['message']['set'][key] = self.parser.serialize(data['message']['set'][key])
            data['message']['set'] = {self.parser.serialize(key) : data['message']['set'][key]}
            data['message'] = {self.parser.serialize('set'): data['message']['set']}
            body = json.dumps(data)
            decodedResponse = await self.fetchResponse(body)
            deserializedResponse = self.parser.deserialize(decodedResponse)
            return deserializedResponse

        elif 'get' in data['message']:
            data['message']['get'] = self.parser.serialize(data['message']['get'])
            data['message'] = {self.parser.serialize('get'): data['message']['get']}
            body = json.dumps(data)
            decodedResponse = await self.fetchResponse(body)
            deserializedResponse = self.parser.deserialize(decodedResponse)
            return deserializedResponse




    # def pingHandler(self, data):
    #     data['message'] = self.parser.serialize(data['message'])


# Example usage:
base_url = "http://localhost:6389"
client = TornadoHttpClient(base_url)

try:
    # Example GET request
    # response_get =  asyncio.run(client.get("ping"))
    # print("GET Response:", response_get)

    # Example POST requests
    data_to_post = {"message": "ping"}
    response_post = asyncio.run(client.post("ping", data=data_to_post))
    print("POST Response:", response_post)

    data_to_post = {"message": {'echo': 'hello world'}}
    response_post = asyncio.run(client.post("echo", data=data_to_post))
    print("POST Response:", response_post)

    data_to_post = {"message": {'set': {'name': 'bismeet'}}}
    response_post = asyncio.run(client.post("set", data=data_to_post))
    print("POST Response:", response_post)

    data_to_post = {"message": {'get': 'name'}}
    getKey = asyncio.run(client.post("get", data=data_to_post))
    print("POST Response:", getKey)


finally:
    client.close()
