import socket
import time
import threading

class Decanter:
  totalAmount = 0
  isResting = False
  totalRuns = 0
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
      Decanter.totalRuns += 1
      print("resting")
      time.sleep(5)
      Decanter.totalAmount -= 10
      Decanter.decantedSubstance += 10

      message = "input-glicerin"
      client.connect(("localhost", 50005))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'glicerin-received' in response:
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
      Decanter.decantedSubstance -= 0.3
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      message = "input-solution"
      client.connect(("localhost", 50008))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'solution-received' in response:
        Decanter.decantedSubstance -= 9.6
      elif b'cannot-receive' in response:
        print("Washer1 can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      Decanter.isResting = False
      
      
    time.sleep(1)
    time_count += 1



main()