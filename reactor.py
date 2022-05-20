import socket
import time
import threading

class Reactor:
  totalAmount = 0
  oil = 0
  naoh = 0
  etoh = 0
  maxOil = 2.5
  maxNaOH = 1.25
  maxEtOH = 1.25

def OpenSocket():
  host = 'localhost'
  port = 50003
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  bindSocket(client, host, port)
  return client

def bindSocket(server, host, port):
  try:
    server.bind((host, port))
    server.listen(100)
    print('server listening on port: ' + str(port))

  #auto reconnection every 3 seconds in case of errors
  except OSError as message:
    print('socket binding error: ' + str(message))
    print('retrying in 3 seconds...\n')
    time.sleep(3)
    bindSocket(server, host, port)

def management(conn, addr):
  print(f"[NEW CONNECTION] {addr} connected.")
  message = conn.recv(1024).decode()
  if 'input-oil' in message and Reactor.oil<=1.75 and Reactor.oil<=Reactor.maxOil:
    Reactor.oil+=0.75
    res = "oil-received"
    print("recebeu")
    print("total oil in reactor: {}".format(Reactor.oil))
    conn.sendall(res.encode())
    conn.close()
  elif 'input-oil' in message and Reactor.oil>1.75:
    res = "cannot-receive"
    conn.sendall(res.encode())
    conn.close()

def main():
  server = OpenSocket()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  

  while True:
    conn, addr = server.accept()
    threading.Thread(target=management(conn, addr), args=(conn, addr))
    
    if time_count%5 == 0:
      print(Reactor.oil)
      
      
    time.sleep(1)
    time_count += 1



main()