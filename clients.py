import socket
import threading
import os
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

HOST = "127.0.0.1"  # server address to connect to
PORT = 6555

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_messages() -> None:
    """
    Continuously listen for incoming data from the server: respond to the
    nickname handshake, and print any regular chat messages as they arrive.
    """
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                logger.info(message)
        except OSError:
            logger.error("Connection to server lost.")
            client.close()
            break


def send_messages() -> None:
    """Continuously read user input and send it to the server as a chat message."""
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode('ascii'))


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()

    write_thread = threading.Thread(target=send_messages, daemon=True)
    write_thread.start()

    try:
        write_thread.join()
    except KeyboardInterrupt:
        logger.error("\nDisconnecting...")
        client.close()
        os._exit(0)