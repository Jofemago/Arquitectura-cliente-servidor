import zmq

#creamos contexto para el cliente
context = zmq.Context()


#creamos socket a partir del contexto
s = context.socket(zmq.REQ)#REQ porque va hacer request(peticiones)


#conectamos en el cliente al socket del server por la ip
s.connect("tcp://127.0.0.1:5002")


msj = "sum,5,5"
s.send(msj.encode('utf-8'))

res = s.recv()

print("respuesta del servidor", res.decode('utf-8'))