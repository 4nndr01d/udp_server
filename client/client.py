import socket
import json
from math import ceil

from typing import Dict, List, Union

from config.consts import SERVER_CONF


class Client:

    def __init__(self):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    @staticmethod
    def __prepare_message(data: dict) -> List[str]:
        raw_data = json.dumps(data)
        parts = []
        package_size = 20

        steps = ceil(len(raw_data) / package_size)
        for i in range(1, steps + 1):
            if i == steps:
                parts.append(raw_data[package_size * (i - 1):])
            else:
                start = package_size * (i - 1) if i > 1 else 0
                parts.append(raw_data[start:package_size * i])
        return parts

    def send_message(self, data: Dict[str, Union[int, float]]) -> None:
        data_parts = self.__prepare_message(data)
        for idx, part in enumerate(data_parts):
            self.send_message_part(part, idx + 1, len(data_parts))

    def send_message_part(self, data: str, idx: int, amount: int) -> None:
        message = {
            'header': {
                # 'marker': "",  # todo Маркер ?????
                # 'num': idx,  # todo Циклический номер сообщения ???(кажется что эти параметры есть в теле)
                'amount': amount,
                'num': idx,
                'size': len(data.encode()),  # Размер блока данных сообщения
            },
            'data': data,
        }
        message = str.encode(json.dumps(message))
        self.sock.sendto(message, SERVER_CONF)
