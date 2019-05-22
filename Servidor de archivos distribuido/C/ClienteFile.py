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
        """Se obtiene hash del archivo y el hash de cada una de sus partes
            y se organiza en un diccionario de la siguiente forma

            sha: hash del archivo
            trozos: lista de los hash de las partes que al unirse forman el archivo
            name: Nombre del archivo

            """
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
        return {'hashfile' : sha1.hexdigest(),
                'trozos' :shas,
                'name' : dir}


    #modificar esta
    def upload(self, i , dir ,data):


        print("conectar con: "+ data['trozos'][i]['server'])
        print("subiendo archivo, espere wey.")
        socketFiles = self.context.socket(zmq.REQ) # creo socket
        socketFiles.connect(data['trozos'][i]['server'])

        with open(path + dir, "rb") as f:

            f.seek(i * self.chunck)
            byte = f.read(self.chunck)
            datas = [b"upload", data['trozos'][i]['hashpart'].encode('utf-8'),byte]
            socketFiles.send_multipart(datas)        #sending chunk to server
            res = socketFiles.recv()
            print(res.decode('utf-8'))
        f.close()

        #hacer un upload de la parte del archivo al server para que el lo guarde

        print("desconectar de: "+ data['trozos'][i]['server'])
        socketFiles.disconnect(data['trozos'][i]['server'])



    def uploadAllFiles(self, data,file):
        """
            data = 'resp': # XXX
                    'info': "###"
                    'hasfile':
                    'trozos':[ {hashpart,ipasignada},
                                       {hashpart,ipasignada},...

                                       ]
        """

        for i in range(len(data['trozos'])):
            self.upload(i, file,data)





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
            """
            res['resp'] = True
            res['info'] = "se guardo el archivo empiece la descarga"
            #res['hashfile'] = datajson['hashfile']
            res['trozos'] = self.UpdateFilesDist(datajson)
            """
            print(resp['info'])
            #print("elementos enviados ", len(x['trozos'])," :\n", x['trozos'])
            #print("elementos enviados ", len(resp['trozos'])," :\n",resp['trozos'])
            ## TODO:
                # empezar carga
            self.uploadAllFiles( resp,file)

        else:
            print(resp['info'])



    def getServerDownload(self, file):

        x = {}
        x['op'] = 'download'
        x['hashfile'] = file

        self.socket.send_json(x)

        res = self.socket.recv_json()
        print(res)

        '''res = {"hasfile": ListToDownload,
                "len": lenListToDownload,#[{haspart:xxx, server:xx}]
                "resp": True,
                "info":"entrega exitosisa debe descargar estos trozos :  " + str(lenListToDownload),
                "name": name
            }
        '''
        #TODO
            #descargar archivos y unirlos





cl = ClienteFile('tcp://127.0.0.1:3001')

cl.getServerUpload('ce.pdf')
#cl.getServerUpload('lb.pdf')
#cl.getServerUpload('thekid.mp4')

#cl.getServerDownload('635ff3d30bc02b55ebfe9b50e0af2bff955b55cd')
#cl.getServerDownload('8cb79739ef1afe81762c4c30ed338229bd8b6843')
