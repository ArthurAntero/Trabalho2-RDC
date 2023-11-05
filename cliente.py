import socket
import threading
import tkinter
from tkinter import simpledialog, messagebox, scrolledtext

def conectar_ao_servidor():
    try:
        global client_socket, username
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP_ADDRESS = '127.0.0.1'
        PORT = 12345
        client_socket.connect((IP_ADDRESS, PORT))
        username = simpledialog.askstring("Username", "Username:", parent=root)
        client_socket.send(username.encode())
        threading.Thread(target=receber_msg).start()
        root.lift()
    except:
        messagebox.showerror("Erro", "Não foi possível se conectar ao servidor.")
        root.destroy()


def enviar_msg():
    recipient = recipient_entry.get()
    message = message_entry.get()
    if message:
        formatted_message = f"{username}:{recipient}:{message}"
        client_socket.send(formatted_message.encode())
        message_entry.delete(0, tkinter.END)

def receber_msg():
    while True:
        try:
            message = client_socket.recv(2048).decode()
            chatbox.configure(state="normal")
            chatbox.insert(tkinter.END, message + "\n")
            chatbox.configure(state="disabled")
            chatbox.see(tkinter.END)
        except:
            messagebox.showinfo("Informação", "Desconectado do servidor.")
            break

def on_closing():
    if client_socket:
        client_socket.close()
    root.destroy()

root = tkinter.Tk()
root.title("Cliente IRC")
root.geometry("400x500")

chatbox = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tkinter.WORD)
chatbox.pack(pady=20)
chatbox.configure(state="disabled")

entry_frame = tkinter.Frame(root)
entry_frame.pack(pady=20)

recipient_label = tkinter.Label(entry_frame, text="Destinatário:")
recipient_label.pack(side=tkinter.LEFT)

recipient_entry = tkinter.Entry(entry_frame, width=20)
recipient_entry.pack(side=tkinter.LEFT, padx=5)

message_entry = tkinter.Entry(entry_frame, width=30)
message_entry.pack(side=tkinter.LEFT, padx=5)

send_button = tkinter.Button(root, text="Enviar", command=enviar_msg)
send_button.pack()

conectar_ao_servidor()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()