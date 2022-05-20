import socket
import time

class EtOHTank:
  etohAmount = 0

def main():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0

  while True:

    # Condition to send a request for oil every 10 seconds 
    # receiving 1 or 2 liters as response randomly
    if time_count%1 == 0:
      message = "get-etoh"
      client.connect(("localhost", 50002))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'input-etoh' in response:
        EtOHTank.etohAmount+=0.25
        print("total de etoh: ", EtOHTank.etohAmount)
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Sends oil to the reactor every second if oilAmount<0.75 and checks if the reactor
    #can receive it
    if time_count%1 == 0:
      if EtOHTank.etohAmount >= 1:
        flowRate = 1
        message = "input-etoh {}".format(flowRate)
        client.connect(("localhost", 50003))
        client.sendall(message.encode())
        response = client.recv(1024)
        if b'etoh-received' in response:
          print("saida realizada com sucesso")
          EtOHTank.etohAmount-=1
        elif b'cannot-receive' in response:
          print("reactor could not receive")
          pass
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
      
    time.sleep(1)
    time_count += 1


main()