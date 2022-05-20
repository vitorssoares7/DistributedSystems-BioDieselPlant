import socket
import time

def main():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  oilAmount = 0

  while True:
    if time_count%5 == 0:
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
    if time_count%1 == 0:
      message = "oi do oiltank1"
      client.connect(("localhost", 50003))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'resposta oiltank2' in response:
        print(response)
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
      
    time.sleep(1)
    time_count += 1


main()