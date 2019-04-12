import zmq
import json

#creamos contexto
context = zmq.Context()

#le solicito un socket al contexto
s = context.socket(zmq.REP)#REP porque va hacer reply(responder por así decirlo)
#conecto el socket a la tarjeta de red '*' por defecto y le asigno un puerto
s.bind('tcp://*:5002')


print("El servidor se encuentra Corriendo.")
#ciclo para poder recibir multiples mensajes, pero es bloqueante
while True:

    
    op, a1, a2 = s.recv_multipart()#operacion bloqueante
    print("recibido del cliente: ",op) 

    #aqui va toda la logica que no quiero hacer jeje

    resp = 'algo'
    s.send(resp.encode('utf-8'))