import zmq
import json
import os

from Server import Server

class ServerFile(Server):


    def __init__(self, ip_puerto, chunck = 1000000):

        Server.__init__(self, ip_puerto)
        self.op = {'getChunk': self.sendChunk , 'exists?':self.exists, 'upload': self.upload, "download": self.download}
        self.chunck = str(chunck)
        self.path = self.makeDirWork()
        self.run() #corro el servidor

    def makeDirWork(self):
        "creo la carpeta y defino el path en donde se van a descargar los archivos"
        path = os.getcwd()
        path = path + '/archivos'

        try:
            os.mkdir(path)
        except OSError:
            print("Creación de carpeta fallida posiblemente ya existe: ", path)
        return path

    def exists(self,data):

        name = data[1].decode('utf-8')
        res, ext = self.existsFile(name)
        res = str(res)
        self.socket.send_multipart([res.encode("utf-8"), ext.encode("utf-8")])

    def existsFile(self, sha1):

        """reviso si existe el archivo en el server
         devuelvo tupla, boolean, string donde el string es la extension del archivo"""
        name,ext = None,None
        for root, dirs, files in os.walk(self.path):
            for filename in files:
                name,ext = filename.split(".")
                if(name == sha1):
                    return True, ext

        return False , ""

    def upload(self,data):
        filesha = data[1].decode('utf-8')
        ext = data[2].decode('utf-8')
        namefile = filesha + "." + ext

        with open(self.path + '/' + namefile, "ab") as f:
            f.write(data[3])

        self.socket.send(b"Recibiendo su archivo, espere...")

    def download(self,data):
        print("recibiendo descarga")
        name = data[1].decode('utf-8')
        with open(self.path + "/"+name, 'rb') as f:
            f.seek(int( data[2].decode('utf-8')))#pos
            byte = f.read(int(self.chunck))

            self.socket.send(byte)



    def sendChunk(self,data):

        self.socket.send(self.chunck.encode('utf-8'))

    def run(self):
        print("Server File is running baby's")
        while True:

            msj = self.socket.recv_multipart()

            assert(len(msj))#debe haber mas de un elemento
            op = msj[0].decode('utf-8')
            print("operacion recibida:", op)
            self.op[op](msj)


sv = ServerFile('tcp://*:5002')
