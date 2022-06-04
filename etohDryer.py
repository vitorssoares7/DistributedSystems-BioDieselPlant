import socket
import time
import threading

class Dryer:
  etoh = 0
  isResting = False

def OpenSocket():
  host = 'localhost'
  port = 50006
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
  if 'input-etoh' in message and Dryer.isResting == False:
    Dryer.etoh += 0.3
    res = "oil-received"
    conn.sendall(res.encode())
    conn.close()
  elif 'input-etoh' in message and Dryer.isResting == True:
    res = "cannot-receive"
    conn.sendall(res.encode())
    conn.close()

def sendEtoh(client):
  print("tentando mandar")
  message = "input-etoh"
  client.connect(("localhost", 50007))
  client.sendall(message.encode())
  response = client.recv(1024)
  if b'etoh-received' in response:
    print("Saida realizada com sucesso")
    Dryer.etoh -= 1
  elif b'cannot-receive' in response:
    print("EtOH tank can not receive")
    pass

def main():
  server = OpenSocket()
  server.settimeout(0.2)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  

  while True:
    try:
      conn, addr = server.accept()
      threading.Thread(target=management(conn, addr), args=(conn, addr))
    except socket.timeout:
      pass
    
    if time_count%1 == 0 and Dryer.etoh >= 1:
      Dryer.isResting = True
      time.sleep(5)
      try:
        sendEtoh(client)
      except:
        sendEtoh(client)
      Dryer.isResting = False
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
    time.sleep(1)
    time_count += 1



main()