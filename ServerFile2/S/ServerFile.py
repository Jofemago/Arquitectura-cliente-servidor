import zmq
import json
import os


from Server import Server

protocol = 'tcp://'

class ServerFile(Server):

    def __init__(self ,ip_port = "127.0.0.1:5000", gb = 1 , numparts = None, ip_proxy = '127.0.0.1:3000',numserver = 0 ):

        Server.__init__(self, protocol + ip_port, protocol + ip_proxy)
        self.op = {}#aqui se definen las operaciones que se hacen por cada tipo de mensaje que recibe el server
        self.numserver = str(numserver)
        self.ip_port =protocol + ip_port#ip y puerto de este servidor
        self.chunksize  =  1024*1024*10  #10MB
        self.gb = gb #1 Gb son 1024MB


        self.info = {   "op" : "registro",
                        "ip" : self.ip_port,#se la mando para que el sepa que direccion debe mandar a los usuarios
                        "gb" : self.gb }

        #self.chuncksize = chunck

        self.numparts  = self.path = self.makeDirWork()

        self.connectToProxy()
        #self.run()



    def connectToProxy(self):

        print("CONECTANDO CON EL PROXY....")
        #msj = json.dump(self.info)
        self.socketProxy.send_json(self.info)
        resp = self.socketProxy.recv().decode()
        print("Numero de partes que el servidor redireccionara: "+ resp)
        return int(resp)




    def makeDirWork(self):
        "creo la carpeta y defino el path en donde se van a descargar los archivos"
        path = os.getcwd()
        path = path + '/archivos'+ self.numserver

        try:
            os.mkdir(path)
        except OSError:
            print("Creación de carpeta fallida posiblemente ya existe: ", path)
        return path


    def run(self):
        print("Server File is running baby's")
        while True:

            msj = self.socket.recv_multipart()



            assert(len(msj))#debe haber mas de un elemento
            op = msj[0].decode('utf-8')
            print("operacion recibida:", op)
            self.op[op](msj)


sf = ServerFile(ip_port = "127.0.0.1:5000", ip_proxy = '127.0.0.1:3000', numserver = 0, gb = 1)
#sf = ServerFile(ip_port = "127.0.0.1:5001", ip_proxy = '127.0.0.1:3000', numserver = 2, gb = 100)
#sf = ServerFile("*:5001",127.0.0.1:3000)
