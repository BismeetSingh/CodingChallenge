class RespParser:

    def __init__(self) -> None:
        pass

    def findSymbol(self, string):
        for i, ch in enumerate(string[1:]):
            if ch == '$' or ch == '*' or ch == '+' or ch == ':' or ch == '*':
                return i + 1
        return -1

    def serialize(self, text):

        if isinstance(text, int):
            return f':{text}\r\n'
        elif isinstance(text, str):
            return f'+{text}\r\n'
        elif isinstance(text, list):
            result = f'*{len(text)}'
            for item in text:
                result += self.serialize(item)
            return result
        elif text is None:
            return '$-1\r\n'

    def deserialize(self, text, ):
        # print(text)
        if isinstance(text, dict):
            output = {}
            for k, v in text.items():
                output[self.deserialize(k)] = self.deserialize(v)
            return output
        else:
            firstChar = text[0]
            data = text[1:]
            # arrays.
            if firstChar == '*':
                result = []
                length, data = text[1:].split('\r\n', 1)
                length = int(length)
                currentArrIndex = 0
                # print(data)
                for i in range(length):
                    symbol = self.findSymbol(data[currentArrIndex:])
                    if symbol != -1:
                        if data[currentArrIndex] != '*':
                            result.append(self.deserialize(text=data[currentArrIndex:currentArrIndex + symbol]))
                        else:
                            # nested arrays
                            result.append(self.deserialize(text=data[currentArrIndex:]))
                        currentArrIndex = symbol + currentArrIndex

                    else:
                        result.append(self.deserialize(text=data[currentArrIndex:]))
                return result

            # simple string case.
            elif firstChar == '+':
                return data.strip()
            # bulk strings
            elif firstChar == '$':  # $ in binary.
                length, text = text[1:].split('\r\n', 1)
                if length == '-1' or length == '0':
                    return None
                text = text.strip()
                return text
            elif firstChar == ':':
                return int(data.strip())

            elif firstChar == '-':
                return None
