import os
import typer

from client import Client
from server import UDPServer
from config import SERVER_CONF, SERVER_MARKER

app = typer.Typer()


@app.command()
def server():
    udp_server = UDPServer(SERVER_CONF)
    udp_server.up()


@app.command()
def send_msg(path: str):
    if not os.path.isfile(path):
        raise 'Файл не найден.'

    data = open(path).read()
    msg_num = 123 # todo Как определять циклический номер сообщения ?
    marker = SERVER_MARKER # todo Маркер, не ясно как определять ?

    client = Client()
    client.send_message(data, msg_num, marker)


if __name__ == "__main__":
    app()
