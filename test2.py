import socket
import time
import threading

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
  if message == "oi do oiltank1":
    print (message)
    res = "resposta oiltank2"
    conn.sendall(res.encode())
    conn.close()

def main():
  server = OpenSocket()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  oilAmount = 0

  while True:
    conn, addr = server.accept()
    threading.Thread(target=management(conn, addr), args=(conn, addr))
    if time_count%3 == 0:
      message = "get-oil"
      client.connect(("localhost", 50002))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'toma oleo' in response:
        print("+1L")
        oilAmount+=1
        print("total de oleo: ", oilAmount)
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
      
    time.sleep(1)
    time_count += 1


main()