import os
import json
import typer

from client import Client
from server import UDPServer
from config import SERVER_CONF

app = typer.Typer()


@app.command()
def server():
    udp_server = UDPServer(SERVER_CONF)
    udp_server.up()


@app.command()
def send_msg(path: str):
    if not os.path.isfile(path):
        raise 'Файл не найден.'

    content = open(path).read()
    data = json.loads(content)

    # Определяем указанное сообщение и передаем
    client = Client()
    client.send_message(data)


if __name__ == "__main__":
    app()
