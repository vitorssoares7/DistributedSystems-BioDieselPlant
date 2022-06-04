import socket
import time
import threading

class Reactor:
  oil = 0
  naoh = 0
  etoh = 0
  processedSubstance = 0
  cicles = 0

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
  message = conn.recv(1024).decode()
  if 'input-oil' in message:
    Reactor.oil+=0.75
    res = "oil-received"
    conn.sendall(res.encode())
    conn.close()
  elif 'input-naoh' in message:
    Reactor.naoh+=1
    res = "naoh-received"
    conn.sendall(res.encode())
    conn.close()
  elif 'input-etoh' in message:
    Reactor.etoh+=1
    res = "etoh-received"
    conn.sendall(res.encode())
    conn.close()


def main():
  server = OpenSocket()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  

  while True:
    conn, addr = server.accept()
    threading.Thread(target=management(conn, addr), args=(conn, addr))
    
    if time_count%1 == 0 and Reactor.oil >= 2.5 and Reactor.naoh >= 1.25 and Reactor.etoh >= 1.25:
      Reactor.oil -= 2.5
      Reactor.naoh -= 1.25
      Reactor.etoh -= 1.25
      Reactor.processedSubstance += 5
      Reactor.cicles+=1
    
    if time_count%10 == 0 and Reactor.processedSubstance >= 10:
      message = "input-substance"
      client.connect(("localhost", 50004))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'substance-received' in response:
        print("Substancia enviada ao decantador")
        Reactor.processedSubstance -= 10
      elif b'cannot-receive' in response:
        print("Decanter can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if time_count%10 == 0:
      message = "Reactor-status:\nNumbers of cicles: {}\n".format(Reactor.cicles)
      client.connect(("localhost", 50002))
      client.sendall(message.encode())
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
    time.sleep(1)
    time_count += 1



main()