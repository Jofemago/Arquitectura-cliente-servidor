import zmq
import json
import os


from Server import Server

protocol = 'tcp://'

class ServerFile(Server):
    
    def __init__(self, ip_port = "*:5000"):

        Server.__init__(self, protocol + ip_port)
        self.op = {}
        self.ip_port = ip_port
        self.gb = gb

        #self.chuncksize = chunck

        self.path = self.makeDirWork()
        self.run()


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

        print("por el momento me bloqueo")
        while True:
            pass

sf = ServerFile("*:5001")