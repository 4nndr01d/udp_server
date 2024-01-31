import random
import socket
import json
import struct

from typing import List

from config.consts import SERVER_CONF, PACKAGE_SIZE


class Client:

    def __init__(self):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    @staticmethod
    def __prepare_message(data: str) -> List[bytes]:
        parts = []
        steps = (len(data) // PACKAGE_SIZE) + 1
        for i in range(0, steps):
            start_idx = i * PACKAGE_SIZE if i != 0 else 0
            part = data[start_idx:PACKAGE_SIZE * (i + 1)]
            parts.append(part.encode('UTF-8'))
        return parts

    def send_message(self, data: str, msg_num: int, marker: int) -> None:
        data = json.dumps(data)
        header = self.get_header(marker, msg_num, len(data.encode("UTF-8")))
        data_parts = self.__prepare_message(data)
        package_marker = random.randint(0, 100) # todo Не ясно, в чем разница от цикл. ном. сообщ. ?

        for idx, part in enumerate(data_parts):
            package_fields = self.get_package_fields(idx + 1, package_marker, len(data_parts), len(part))

            message = header + package_fields + part
            self.sock.sendto(message, SERVER_CONF)

    @staticmethod
    def get_header(marker: int, num: int, size: int) -> bytes:
        return struct.pack('!III', marker, num, size)

    @staticmethod
    def get_package_fields(num: int, marker: int, amount: int, size: int):
        return struct.pack('!IIII', marker, amount, num, size)
