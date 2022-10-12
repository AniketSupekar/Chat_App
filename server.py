import socket 
import threading 
import tkinter 
import tkinter.scrolledtext
from tkinter import*


host='localhost'
#host='192.168.43.77'
port=9000

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
usernames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message= client.recv(1024)
            print(f'{usernames [clients.index(client)]} : {message}')
            broadcast(message)

        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            username=usernames[index]
            usernames.remove(username)
            break

'''active_connections=Tk()
Connected_clients=Listbox(active_connections)
Connected_clients.insert(usernames)
Connected_clients.pack()
active_connections.mainloop()'''



def recieve():
    while True:
        client, address= server.accept()
       
        print("connected with", address)

        client.send('USER'.encode('ascii'))
        username=client.recv(1024)

        usernames.append(username)
        clients.append(client)

        print("Username of the client is", username)
        broadcast(f'{username}\n' .encode('ascii'))
      

        thread=threading.Thread(target=handle_client, args=(client,))
        thread.start()

        print(f'Active connections: {threading.activeCount()-1}')
        print(usernames)
        '''active_connections=Tk()
        Connected_clients=Listbox(active_connections)
        Connected_clients.insert(-1,usernames)
        Connected_clients.yview_scroll(1,'units')
        Connected_clients.pack()
        active_connections.mainloop()'''

print("Server is ready")

recieve()