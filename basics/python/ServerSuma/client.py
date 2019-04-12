import zmq
import json

#creamos contexto para el cliente
context = zmq.Context()


#creamos socket a partir del contexto
s = context.socket(zmq.REQ)#REQ porque va hacer request(peticiones)
#conectamos en el cliente al socket del server por la ip
s.connect("tcp://127.0.0.1:5002")


#msj = "sum,5,5"
#msj = {"operacion":"suma", "a1":10, "a2":20}
msj = [ b"suma", b"3", b"4"] 
#s.send(msj.encode('utf-8'))
s.send_multipart(msj)



res = s.recv()

print("respuesta del servidor", res.decode('utf-8'))