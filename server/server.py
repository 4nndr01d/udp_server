import json
import socket

from typing import Tuple

from config.consts import BUFFER_SIZE


class UDPServer:

    def __init__(self, conf: Tuple[int, str]):
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server.bind(conf)
        self.messages = {}

    def up(self) -> None:
        print("UDP server up and listening")

        while True:
            bytes_address_pair = self.server.recvfrom(BUFFER_SIZE)
            message = bytes.decode(bytes_address_pair[0])
            message = json.loads(message)
            address = bytes_address_pair[1]

            print(f"Client {address[0]} send message.")
            self.__set_message(address, message)
            if self.is_last_message(message):
                if message['header']['amount'] != len(self.messages[address[0]]):
                    print('Invalid package list.')
                else:
                    self.collect_packages(address[0])

    def __set_message(self, address: tuple, message: str):
        if address[0] in self.messages:
            self.messages[address[0]][message['header']['num']] = message['data']
        else:
            self.messages[address[0]] = {
                message['header']['num']: message['data'],
            }

    @staticmethod
    def is_last_message(message) -> bool:
        return message['header']['num'] == message['header']['amount']

    def collect_packages(self, address):
        full_data = ''.join([self.messages[address][i] for i in self.messages[address]])
        full_data = json.loads(full_data)
        print(full_data)
