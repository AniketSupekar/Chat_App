import socket
import threading 
import tkinter 
import tkinter.scrolledtext
from tkinter import simpledialog 
from tkinter import* 

host='localhost'
port=9000

class Client:
    def _init_(self, host, port):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))

        msg=tkinter.Tk()
        msg.withdraw() 
        self.username=simpledialog.askstring("SERVER BASED CHAT ROOM", "Please choose a username", parent=msg)
        
        self.finish= False
        self.running= True

        thread1= threading.Thread(target=self.loop)
        thread2= threading.Thread(target=self.receive)

        thread1.start()
        thread2.start()
    def loop(self): 

        self.win=tkinter.Tk()
        self.win.configure(bg="lavender")

        self.label = tkinter.Label(self.win, text="Your Conversations:", bg="lavender")
        self.label.config(font=("Serif",12))
        self.label.pack(padx=20, pady=5)


        self.chat_field=tkinter.scrolledtext.ScrolledText(self.win)
        self.win.title("LETS CHAT")
        self.chat_field.pack(padx=10, pady=5)
        self.chat_field.config(state='disabled')

        self.msg_back = tkinter.Label(self.win, text="Type your message:", bg="lavender")
        self.msg_back.config(font=("Serif",12))
        self.msg_back.pack(padx=20, pady=5)

        self.input= tkinter.Text(self.win, height=3)
        self.input.pack(padx=10, pady=5)

        self.send_button= tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Serif",12))
        self.send_button.pack(padx=10, pady=5)

        self.finish=True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        message=f"{self.username}: {self.input.get('1.0', 'end')}"
        self.sock.send(message.encode('ascii'))
        self.input.delete('1.0','end')

    def stop(self):
        self.running= False
        self.win.destroy()
        self.sock.close()
        exit(0)

    
    def receive(self):
        while self.running:
            try:
                message=self.sock.recv(1024).decode('ascii')
                if message=='USER':
                    self.sock.send(self.username.encode('ascii'))

                else:
                    if self.finish:
                        self.chat_field.config(state='normal')
                        self.chat_field.insert('end', message)
                        self.chat_field.yview('end')
                        self.chat_field.config(state='disabled')

            except ConnectionAbortedError:
                break

            except:
                print('Error')
                break

client=Client(host,port)
