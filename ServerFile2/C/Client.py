import zmq
import json

class Client():
    """
        username: name of user
        ip_puerto: example "tcp://127.0.0.1:5002"
    """
    def __init__(self, ip_puerto):



        self.ip_puerto = ip_puerto
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.ip_puerto)
        



if __name__ == "__main__":


    #cl = Client("tcp://127.0.0.1:5002")
    msj = b'Mensaje de prueba'
    print('se envia el mensaje', msj.decode('utf-8'))
    cl.socket.send(msj)
    res = cl.socket.recv()
    print('Respuesta del server', res.decode('utf-8'))
