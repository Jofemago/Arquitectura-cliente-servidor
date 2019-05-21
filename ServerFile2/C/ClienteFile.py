import zmq
import zmq
import json
import os



protocol = 'tcp://'



from Client import Client


class ClienteFile(Client):

    def __init__(self, ip_puerto):

        Client.__init__(self, ip_puerto)
        self.chunk = 1024*1024*10

    def getChunck(self):
        """Se obtiene por parte del servidor el tamaño en bytes de
        de cada paquete que se envie."""

        msj = [b"getChunk"]#crear json
        self.socket.send_multipart(msj)
        print("solicitando tamaño de envio")

        ch = self.socket.recv()
        print(ch)
        ch = ch.decode('utf-8')
        return int(ch)





cl = ClienteFile("tcp://127.0.0.1:5002")
