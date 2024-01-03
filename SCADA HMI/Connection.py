import socket
import threading
import time


class ConnectionHandler(object):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    isConnected = False
    connection_lock = threading.RLock()
    connected, lostConnection = threading.Condition(connection_lock), threading.Condition(connection_lock)
    """def connect(client,base_info):
    try:
        client.connect(('127.0.0.1', int(base_info["num_port"])))
        isConnected = True
        return isConnected
    except ConnectionRefusedError:
        print("Could not connect to the server. Server may not be running or address/port is incorrect.")
        isConnected = False
        return isConnected
    except Exception as e:
        print(f"An error occurred: {e}")
        isConnected = False
        return isConnected"""


def connect_thread(base_info, foo):
    while True:
        if ConnectionHandler.isConnected == False:
            with ConnectionHandler.connection_lock:
                try:
                    ConnectionHandler.client.connect(('127.0.0.1', int(base_info["num_port"])))
                    ConnectionHandler.isConnected = True
                    ConnectionHandler.connected.notify_all()
                    ConnectionHandler.lostConnection.wait()
                    ConnectionHandler.client.close()
                    ConnectionHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    ConnectionHandler.isConnected = False
                    time.sleep(0.5)


def disconnect(client):
    client.close()
    return True
