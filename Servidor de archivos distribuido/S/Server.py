
import zmq


#'tcp://*:5002'
class Server():

    def __init__(self, ip_puerto, ip_proxy):

        self.ip_puerto = ip_puerto
        self.ip_proxy = ip_proxy
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(self.ip_puerto)

        #agrego socket REQ para hacer la conexion y pasar la informacion al proxy
        self.socketProxy = self.context.socket(zmq.REQ)
        self.socketProxy.connect(self.ip_proxy)


if __name__ == "__main__":
    server = Server('tcp://*:5002')

    print("este server esta corriendo")
    while True:

        arrive = server.socket.recv()
        print('recibido del cliente', arrive.decode('utf-8'))

        resp = b"respondo bien"
        server.socket.send(resp)
