import zmq
import json
import os


from Server import Server


class Proxy(Server):

    def __init__(self, ip_puerto):

        Server.__init__(self, ip_puerto)
        self.op = { "registro": self.registroServer,
                    "upload": self.setServersChunks,
                    "download": self.downloadFileDist}


        #creo una lista donde voy a guardar todos los servidores
        self.servers = []

        self.filesDist = {}
        self.filesDistNames = {}
        '''
            self.filesDist = {hashfile: [ {hashpart:ipasignada},
                        {hashpart:ipasignada},...

                        ]
            }
            self.filesDist = {hashfile: name}
        '''
        #self.path = self.makeDirWork()
        self.run()


    def getNumParts(self):
        """Cuenta el numero de partes disponibles en los servidor"""
        total = 0
        for sv in self.servers:
            total += sv['partes']

        return total


    def downloadFileDist(self,datajson):
        """
            datajson = {
                            "op": "download",
                            "hashfile": hash
                        }
        """
        if datajson["hashfile"] in self.filesDist:
            """si el hash existe se envia la info de los servers, de lo contrario no se hace"""

            print("enviando informacion de nodos distruidos")
            ListToDownload = self.filesDist[datajson["hashfile"]]
            lenListToDownload = len(ListToDownload)
            name = self.filesDistNames[datajson["hashfile"]]
            print("descargando archivo: ", datajson["hashfile"], " name: ",name )
            res = {"hasfile": ListToDownload,
                    "len": lenListToDownload,#[{haspart:xxx, server:xx}]
                    "resp": True,
                    "info":"entrega exitosisa debe descargar estos trozos :  " + str(lenListToDownload),
                    "name": name
                }
            self.socket.send_json(res)

        else:
            print("intento de descarga, no existe el archivo")
            res = {"hasfile": None,
                    "len": None,
                    "resp": False,
                    "info":"entrega fallida: " + str(0)
                    }
            self.socket.send_json(res)



    def UpdateFilesDist(self,datajson):
        """
            recibe:
            datajson -> {   'hashfile' : sha1.hexdigest(),
                            'trozos' :shas,
                            'name' : dir
                        }
            hash de archivo que se desea subir y hash de cada una de sus partes

            configura la variable self.filesDist agregando un elemento al diccionario

             self.filesDist = {hashfile: [ {hashpart:ipasignada},
                                {hashpart:ipasignada},...

                                ]
                    }
        """

        print('update filesDist',datajson['hashfile'])
        enlace = []
        for sha in datajson['trozos']:


            sv = self.servers.pop()#saca el ultimo server para asignarle carga
            if sv['partes'] > 0: #si el servidor tiene partes le puede mandar uno de los chunck
                x = {
                        'hashpart': sha,
                        'server': sv['ip']
                    }
                enlace.append(x)
                sv['partes'] -= 1#coomo va enviar uno se lo resta
                self.servers.insert(0, sv) #lo regresa a la cola, en espera de turnos
            else: #el server que estamos tratando es igual a 0 :O

                self.servers.insert(0, sv)
                bool = True
                while bool:

                    sv = self.servers.pop()#saca el ultimo server para asignarle carga
                    if sv['partes'] > 0: #si el servidor tiene partes le puede mandar uno de los chunck
                        x = {
                                'hashpart': sha,
                                'server': sv['ip']
                            }
                        enlace.append(x)
                        sv['partes'] -= 1#coomo va enviar uno se lo resta

                        bool = False
                    self.servers.insert(0, sv) #lo regresa a la cola, en espera de turnos


        self.filesDist[datajson['hashfile']] = enlace
        self.filesDistNames[datajson['hashfile']] = datajson['name']
        print('Nombre archivo:  ', datajson['name'])
        return enlace



    def setServersChunks(self, datajson):
        """
            recibe:
            datajson -> {   'hashfile' : sha1.hexdigest(),
                            'trozos' :shas,
                            'name' : dir
                        }

            si no existe el sha lo agrega y le asigna el servidor donde sera almacenado el chunk
            si y solo si existen servidores disponibles
        """
        print('upload')
        res = {}
        parts = self.getNumParts()
        print("cantidad de chunks disponibles antes de la carga: ",parts)
        if parts < len(datajson['trozos']):

            res['resp'] = False #no hay archivos cargados no se puede subir nada
            res['info'] = "no hay servidores disponibles, intentelo mas tarde"
            self.socket.send_json(res)
            print('capacidad llena')

        elif datajson['hashfile'] in self.filesDist:

            res['resp'] = False #no hay archivos cargados no se puede subir nada
            res['info'] = "Este archivo ya existe, no se permite subir dos veces"
            self.socket.send_json(res)
            print('intento de sobrescritura')

        else:
            #asignamos servers y actualizamos la distribucion de servidores
            print('cantidad de archivos: ', len(self.filesDist), " + 1" )
            #To Do

            #subir uno y probar si con el mismo muestra el if del medio
            res['resp'] = True
            res['info'] = "se guardo el archivo empiece la descarga"

            res['trozos'] = self.UpdateFilesDist(datajson)

            self.socket.send_json(res)
            parts = self.getNumParts()
            print("cantidad de chunks disponibles luego de la carga: ", parts)



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
