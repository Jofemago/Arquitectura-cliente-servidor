import zmq
import json
import os


from Server import Server


class Proxy(Server):

    def __init__(self, ip_puerto):

        Server.__init__(self, ip_puerto)
        self.op = {"registro": self.registroServer}


        #creo una lista donde voy a guardar todos los servidores
        self.servers = []


        #self.path = self.makeDirWork()
        self.run()

    def registroServer(self, datajson):
        '''Con esta funcion se logra que un server quede registrado
            en una lista donde estaran todos los server y su cantidad de partes'''

        print('registrar:\n', datajson)

        partes = int((datajson['gb']*1024)/10)
        print('cantidad partes: ',partes)
        server = {  'ip': datajson['ip'],
                    'partes': partes} #cantidad de partes disponibles por server
        self.servers.append(server)

        print('servers: ', self.servers)
        partes = str(partes)
        self.socket.send(partes.encode())




    def makeDirWork(self):
        "creo la carpeta y defino el path en donde se van a descargar los archivos"
        path = os.getcwd()
        path = path + '/archivos'

        try:
            os.mkdir(path)
        except OSError:
            print("Creación de carpeta fallida posiblemente ya existe: ", path)
        return path

    def run(self):
        print("The proxy is running")


        while True:

            res = self.socket.recv_json()
            #print(res)
            #res = json.loads(res)

            print("operacion: " + res['op'])
            self.op[res['op']](res)







proxy = Proxy('tcp://127.0.0.1:3000')
