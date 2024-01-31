import json
import socket
import struct

from typing import Tuple

from config.consts import BUFFER_SIZE, SERVER_MARKER


class UDPServer:

    def __init__(self, conf: Tuple[int, str]):
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server.bind(conf)
        self.messages = {}

    def up(self) -> None:
        print("UDP server up and listening")

        while True:
            msg, sender_address = self.server.recvfrom(BUFFER_SIZE)
            address = sender_address[0]

            print(f"Client {address} send message.")
            header, package_fields, message = self.unpack_message(msg)
            if header[0] == SERVER_MARKER:
                self.__set_message(address, message, package_fields)
                if self.is_last_message(package_fields):
                    if package_fields[1] != len(self.messages[address][package_fields[0]]):
                        print('Invalid package list.')
                    else:
                        self.collect_packages(address, package_fields[0])

    def unpack_message(self, message: bytes) -> tuple:
        return (
            struct.unpack("!III", message[:12]),
            struct.unpack("!IIII", message[12:28]),
            message[28:].decode("UTF-8"),
        )

    def __set_message(self, address: tuple, message: str, fields: Tuple[int]) -> None:
        if address in self.messages:
            if fields[0] not in self.messages[address]:
                self.messages[address][fields[0]] = {}
            self.messages[address][fields[0]][fields[2]] = message
        else:
            if address not in self.messages:
                self.messages[address] = {}
            self.messages[address][fields[0]] = {
                fields[2]: message,
            }

    @staticmethod
    def is_last_message(fields: dict) -> bool:
        return fields[1] == fields[2]

    def collect_packages(self, address, data_marker: str):
        full_data = ''.join([self.messages[address][data_marker][i] for i in self.messages[address][data_marker]])
        full_data = json.loads(full_data)
        print(full_data)
