import zmq
import json
import hashlib
import os
import sys
from Client import Client

class ClientFile(Client):

    def __init__(self, ip_puerto):

        Client.__init__(self,ip_puerto) #con esto se abre el canal de comunicacion
        self.chunck = self.getChunck()
        print("tamaño de envio establecido,", self.chunck)

    def getChunck(self):
        """Se obtiene por parte del servidor el tamaño en bytes de
        de cada paquete que se envie."""

        msj = [b"getChunk"]
        self.socket.send_multipart(msj)
        print("solicitando tamaño de envio")

        ch = self.socket.recv()
        ch = ch.decode('utf-8')
        return int(ch)


    def UploadFile(self, dir):

        """Preparación  y subida de archivos"""
        name, ext = dir.split(".")
        sha1 = self.makeSHAFile(dir)

        data = [b"exists?", sha1.encode('utf-8')]
        
        self.socket.send_multipart(data)

        res = self.socket.recv_multipart()
        
        if res[0].decode('utf-8') == 'False':
            self.upload(dir, name, ext, sha1)
        else:
            print("ese archivo ya existe en el servidor, no se haga coger fastidio papi")
            

    def upload(self, dir, name, ext, filesha):

        print("subiendo archivo, espere wey.")
        with open(dir, "rb") as f:
            while True:
                byte = f.read(self.chunck)
                if not byte:
                    break
                data = [b"upload", filesha.encode('utf-8'), ext.encode('utf-8'),byte] 
                self.socket.send_multipart(data)        #sending chunk to server
                res = self.socket.recv()
                print(res.decode('utf-8'))
        print("Guarde este hash para descargar y compartir:", filesha)


    def downloadFile(self, filesha):

        data = [b"exists?", filesha.encode('utf-8')]
        
        self.socket.send_multipart(data)

        res = self.socket.recv_multipart()
        
        if res[0].decode('utf-8') == 'False':

            print("no existe el archivo, se cancela la descarga")
        
        else:
            self.download(filesha, res[1].decode('utf-8'))


    def download(self,filesha, ext):

        name = filesha + "." + ext
        data = [b"download", name.encode('utf-8')]
        with open(name, "wb") as f:
            self.socket.send_multipart(data)
            while True:

                byte = self.socket.recv()
                if not byte:
                    print("se recibió todo el archivo")
                    break
                f.write(byte)
                self.socket.send(b"El cliente esta recibiendo wey")




    def makeSHAFile(self, dir):
        sha1 = hashlib.sha1()
        with open(dir, "rb") as f:
            while True:
                byte = f.read(self.chunck)
                if not byte:
                    break
                sha1.update(byte)
        return sha1.hexdigest()      
                



cl = ClientFile("tcp://127.0.0.1:5002")


#cl.UploadFile("image.png")
#cl.UploadFile("kid.mp4")
#cl.downloadFile('9116b54370461ead5aaa10dc5b572d44dbbb7b6f')
cl.downloadFile('983b2f644610fd9e75fd27c9fe29d4b8896fee0c')

