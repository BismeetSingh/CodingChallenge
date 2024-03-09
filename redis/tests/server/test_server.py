import unittest
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from unittest.mock import patch
from server.server import RedisHandler, make_app
import json


class TestRedisHandler(AsyncHTTPTestCase):

    def get_app(self):
        return make_app()

    @patch('server.server.RespParser')
    @gen_test
    async def test_post_request_ping(self, mock_parser):
        mock_parser.return_value.deserialize.return_value = 'ping'
        mock_parser.return_value.serialize.return_value = '+pong\r\n'
        message = {"message": "+ping\r\n"}
        response = await self.http_client.fetch(
            self.get_url('/ping'),
            method='POST',
            body=json.dumps(message))

        self.assertEqual(response.code, 200)  # Adjust the expected status code accordingly
        self.assertEqual(response.body, b'+pong\r\n')

    @patch('server.server.RespParser')
    @gen_test(timeout=20)
    async def test_post_request_set_and_get(self, mock_parser):
        mock_parser.return_value.deserialize.return_value = {'set' : {'name': 'bismeet'}}
        mock_parser.return_value.serialize.return_value = '+OK\r\n'
        message = {"message": {"+set\r\n"  : {"+name\r\n": "+bismeet\r\n"}}}
        response = await self.http_client.fetch(
            self.get_url('/set'),
            method='POST',
            body=json.dumps(message))

        self.assertEqual(response.code, 200)  # Adjust the expected status code accordingly
        self.assertEqual(response.body, b'+OK\r\n')

        mock_parser.return_value.deserialize.return_value = {'get': 'name'}
        mock_parser.return_value.serialize.return_value = '+bismeet\r\n'
        message = {"message": {"+get\r\n": "+name\r\n"}}
        response = await self.http_client.fetch(
            self.get_url('/get'),
            method='POST',
            body=json.dumps(message))

        self.assertEqual(response.code, 200)  # Adjust the expected status code accordingly
        self.assertEqual(response.body, b'+bismeet\r\n')

    @patch('server.server.RespParser')
    @gen_test(timeout=20)
    async def test_post_request_set_and_get_invalid_key(self, mock_parser):
        mock_parser.return_value.deserialize.return_value = {'set': {'name': 'bismeet'}}
        mock_parser.return_value.serialize.return_value = '+OK\r\n'
        message = {"message": {"+set\r\n": {"+name\r\n": "+bismeet\r\n"}}}
        response = await self.http_client.fetch(
            self.get_url('/set'),
            method='POST',
            body=json.dumps(message))

        self.assertEqual(response.code, 200)  # Adjust the expected status code accordingly
        self.assertEqual(response.body, b'+OK\r\n')

        mock_parser.return_value.deserialize.return_value = {'get': 'dummy'}
        mock_parser.return_value.serialize.return_value = '+Nil\r\n'
        message = {"message": {"+get\r\n": "+dummy\r\n"}}
        response = await self.http_client.fetch(
            self.get_url('/get'),
            method='POST',
            body=json.dumps(message))

        self.assertEqual(response.code, 200)  # Adjust the expected status code accordingly
        self.assertEqual(response.body, b'+Nil\r\n')
    # Add more assertions as needed

    @patch('server.server.RespParser')
    @gen_test
    async def test_post_request_echo(self, mock_parser):
        mock_parser.return_value.deserialize.return_value = {'echo': 'hello'}
        mock_parser.return_value.serialize.side_effect =[ '+echo\r\n', '+hello\r\n']
        message = {"message": {"+echo\r\n" : "+hello\r\n"}}
        response = await self.http_client.fetch(
            self.get_url('/echo'),
            method='POST',
            body=json.dumps(message))

        self.assertEqual(response.code, 200)  # Adjust the expected status code accordingly
        self.assertEqual(json.loads(response.body), {'message': {'+echo\r\n': '+hello\r\n'}})
