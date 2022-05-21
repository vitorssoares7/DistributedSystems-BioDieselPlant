import socket
import time
import threading

class Decanter:
  totalAmount = 0
  isResting = False
  decantedSubstance = 0

def OpenSocket():
  host = 'localhost'
  port = 50004
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
  if 'input-substance' in message and Decanter.isResting == False:
    Decanter.totalAmount+=10
    res = "substance-received"
    conn.sendall(res.encode())
    conn.close()
  elif 'input-substance' in message and Decanter.isResting == True:
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
    
    if time_count%1 == 0 and Decanter.totalAmount == 10:
      Decanter.isResting = True
      print("resting")
      time.sleep(5)
      Decanter.totalAmount -= 10
      Decanter.decantedSubstance += 10
      print(Decanter.decantedSubstance)

      message = "input-glicerin"
      client.connect(("localhost", 50005))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'glicerin-received' in response:
        print("Saida realizada com sucesso")
        Decanter.decantedSubstance -= 0.1
      elif b'cannot-receive' in response:
        print("Glicerin tank can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      message = "input-etoh"
      client.connect(("localhost", 50006))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'etoh-received' in response:
        print("Saida realizada com sucesso")
        Decanter.decantedSubstance -= 0.3
      elif b'cannot-receive' in response:
        print("EtOH dryer not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      print(Decanter.decantedSubstance)
      Decanter.isResting = False

      # message = "input-glicerin"
      # client.connect(("localhost", 50005))
      # client.sendall(message.encode())
      # response = client.recv(1024)
      # if b'glicerin-received' in response:
      #   print("Saida realizada com sucesso")
      #   Decanter.decantedSubstance -= 1
      # elif b'cannot-receive' in response:
      #   print("Glicerin tank can not receive")
      #   pass
      # client.close()
      # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
      
    time.sleep(1)
    time_count += 1



main()