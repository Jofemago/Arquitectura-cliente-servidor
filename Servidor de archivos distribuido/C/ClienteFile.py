import zmq
import json
import os
import hashlib
import sys


protocol = 'tcp://'
path = os.getcwd() +'/archivos/'


from Client import Client


class ClienteFile(Client):

    def __init__(self, ip_puerto):

        Client.__init__(self, ip_puerto)
        self.chunck = 1024*1024*10

    def makeSHAFile(self, dir):
        sha1 = hashlib.sha1()
        shas = []
        with open(path + dir, "rb") as f:
            while True:
                byte = f.read(self.chunck)
                if not byte:
                    break

                sha2 = hashlib.sha1()
                sha2.update(byte)
                shas.append(sha2.hexdigest())

                sha1.update(byte)
        print("cantidad de trozos que genera el archivo para upload: ",len(shas))
        return {'sha' : sha1.hexdigest(),
                'trozos' :shas,
                'name' : dir}


    def getServerUpload(self, file):
        """En caso tal de que se pueda hacer la descargar
        y no exista el archivo ya en el sistema
        el servidor proxy asignara a cada trozo un sitio donde deba guardarse"""

        x = self.makeSHAFile( file)
        x['op'] = 'upload'

        self.socket.send_json(x)
        #print(x)

        resp = self.socket.recv_json()
        if(resp['resp']):
            pass
        else:
            print(resp['info'])




cl = ClienteFile('tcp://127.0.0.1:3001')

cl.getServerUpload('lb.pdf')
