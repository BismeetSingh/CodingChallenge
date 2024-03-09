from parsers.resp_parser import RespParser
from unittest import TestCase


class RespParserTests(TestCase):

    def setUp(self):
        self.resp_parser = RespParser()


class SerializerTests(RespParserTests):

    def testSerializeInteger(self):
        input = 345
        result = self.resp_parser.serialize(input)
        self.assertEqual(result, f':{input}\r\n')

    def testSerializeSimpleString(self):
        input = 'hello world'
        result = self.resp_parser.serialize(input)
        self.assertEqual(result, f'+{input}\r\n')

    def testSerializeArray(self):
        input = ['hello', 'worlds', 'bismeet']
        result = self.resp_parser.serialize(input)
        self.assertEqual(result, '*3+hello\r\n+worlds\r\n+bismeet\r\n')

    def testSerializeArrayWithInteger(self):
        input = ['hello', 'worlds', 2]
        result = self.resp_parser.serialize(input)
        self.assertEqual(result, '*3+hello\r\n+worlds\r\n:2\r\n')

    def testNoneSerialized(self):
        result = self.resp_parser.serialize(None)
        self.assertEqual(result, '$-1\r\n')


class DeSerializerTests(RespParserTests):

    def testSimpleStringDeserialize(self):
        input = '+hello world\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertEqual(result, 'hello world')

    def testBulkStringDeserialize(self):
        basic_string = 'hellgo'
        length_binary_string = len(basic_string)
        input = f'${length_binary_string}\r\n{basic_string}\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertEqual(result, 'hellgo')

    def testBulkStringWithNilValueReturnsNone(self):
        length_binary_string = -1
        input = f'${length_binary_string}\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertIsNone(result)

    def testBulkStringWithZeroLengthReturnsNone(self):
        length_binary_string = 0
        input = f'${length_binary_string}\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertIsNone(result)

    def testDeserializeInteger(self):
        input = ':42\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertEqual(result, 42)

    def testDeserializeArraysWithBulkStrings(self):
        input = '*3\r\n$5\r\nhello\r\n$6\r\nworlds\r\n$7\r\nbismeet\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertEqual(result, ['hello', 'worlds', 'bismeet'])

    def testDeserializeIntArrays(self):
        input = '*3\r\n:1\r\n:2\r\n:3\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertEqual(result, [1, 2, 3])

    def testDeseralizeIntWithBulkStringArray(self):
        input = '*2\r\n$5\r\nhello\r\n:33\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertEqual(result, ['hello', 33])

    def testDeseralizeNestedArrays(self):
        input = '*3\r\n$6\r\nfruits\r\n$5\r\napple\r\n*2\r\n$5\r\niphone\r\n$4\r\nipad\r\n'
        result = self.resp_parser.deserialize(input)
        self.assertEqual(result, ['fruits', 'apple', ['iphone', 'ipad']])

    def testDeserializeErrorMessage(self):
        text = "-Error message\r\n"
        result = self.resp_parser.deserialize(text)
        self.assertEqual(result, None)
