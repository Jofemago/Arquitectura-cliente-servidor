import zmq
import json
import os


from Server import Server


class Proxy(Server):

    def __init__(self, ip_puerto):

        Server.__init__(self, ip_puerto)
        self.op = { "registro": self.registroServer,
                    "upload": self.configureServers}


        #creo una lista donde voy a guardar todos los servidores
        self.servers = []
        self.filesDist = {}


        #self.path = self.makeDirWork()
        self.run()


    def getNumParts(self):
        """Cuenta el numero de partes disponibles en el servidor"""
        total = 0
        for sv in self.servers:
            total += sv['partes']

        return total


    def configureServers(self, datajson):

        res = {}
        parts = self.getNumParts()
        if parts < len(datajson['trozos']):
            res['resp'] = False #no hay archivos cargados no se puede subir nada
            res['info'] = "no hay servidores disponibles, intentelo mas tarde"
            self.socket.send_json(res)

        elif datajson['sha'] in self.filesDist:

            res['resp'] = False #no hay archivos cargados no se puede subir nada
            res['info'] = "Este archivo ya existe, no se permite subir dos veces"
            self.socket.send_json(res)

        else:
            #To Do
            #asignar direccion ip a cada uno de los trozos
            #almacenarlo en self.servers
            #subir uno y probar si con el mismo muestra el if del medio

            pass



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




    '''def makeDirWork(self):
        "creo la carpeta y defino el path en donde se van a descargar los archivos"
        path = os.getcwd()
        path = path + '/archivos'

        try:
            os.mkdir(path)
        except OSError:
            print("Creación de carpeta fallida posiblemente ya existe: ", path)
        return path'''

    def run(self):
        print("The proxy is running")


        while True:

            res = self.socket.recv_json()
            #print(res)
            #res = json.loads(res)

            print("operacion: " + res['op'])
            self.op[res['op']](res)







proxy = Proxy('tcp://127.0.0.1:3001')
