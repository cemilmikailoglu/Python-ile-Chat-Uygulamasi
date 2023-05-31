import tkinter as tk
import socket
import threading
import time

# * İP ADRESİ MANUEL OLARAK DEĞİŞTİRİLMELİDİR SERVER AÇILDIĞINDA VERİLEN İP ÜZERİNDEN AÇILMALIDIR
HOST = '192.168.220.89'
PORT = 8080

def connect(even=None):
    global username
    global s
    global err1
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        t = threading.Thread(target=listen)
        t.start()
    except ConnectionRefusedError:
        errorText = "Bağlantı oluşamadı! Server kapalı olabilir."
        print(errorText)

        return
    except:
        errorText = "anlaşılmayan bir hata oluştu"
        print(errorText)
        return

    if " " in user_name_entry.get():
        if not err1:
            errorText = "Kullanıcı adında boşluk olamaz!"
            eror_label1.config(text=errorText)
            eror_label1.pack(ipady=(10))
            err1 = True
        else:
            eror_label1.config(fg="white")
            time.sleep(0.2)
            eror_label1.config(fg="red")
        return    
    username = user_name_entry.get()
    eror_label1.pack_forget()
    #*- delete username form----
    user_name_entry.pack_forget()
    user_name_frame.pack_forget()
    connect_button.pack_forget()

    #*- resize form----
    root.geometry("400x300")
    chat_frame.pack(padx=10, pady=10)
    chat_label.pack(side=tk.LEFT)
    chat_box.pack(side=tk.LEFT)
    message_frame.pack(padx=10, pady=10)
    message_label.pack(side=tk.LEFT)
    message_entry.pack(side=tk.LEFT)
    message_entry.bind('<Return>', send_message)
    send_button.pack(side=tk.LEFT)


def listen():
    while True:
        try:
            message = s.recv(1024)
            if message:
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, message.decode('utf-8'))
                chat_box.see(tk.END)
                chat_box.config(state=tk.DISABLED)
        except:
            break

def send_message(event=None):
    global username
    message = message_entry.get()
    if message != "":
        # kullaniciadi = user_name_entry.get()
        message = "\n" + username + ": " + message
        s.send(message.encode('utf-8'))
        message_entry.delete(0, tk.END)
        chat_box.see(tk.END)

def on_close(even=None):
    global username
    global a
    a += 1
    if a == 13:
        message = f"{username} sohbetten ayrıldı! güle güle"
        message = "\n" + message
        s.send(message.encode('utf-8'))
        print("closed")
        s.close()
        root.quit()

root = tk.Tk()
root.config(background="orange")
root.resizable(False, False)
root.geometry("200x100")
root.title("Sohbet Uygulaması")
user_name_frame = tk.Frame(root)
user_name_frame.pack(padx=20, pady=20)    
user_name_label = tk.Label(user_name_frame, text="Kullanıcı Adı:", bg='orange')
user_name_label.pack(side=tk.LEFT)

user_name_entry = tk.Entry(user_name_frame, width=15)   
user_name_entry.pack(side=tk.TOP)
connect_button = tk.Button(root, text="Bağlan", command=connect)
connect_button.pack()
user_name_entry.bind('<Return>', connect)

chat_frame = tk.Frame(root)
chat_label = tk.Label(chat_frame, text="Sohbet:")
chat_box = tk.Text(chat_frame, width=50, height=15, state=tk.DISABLED)
#* ERR
eror_label1 = tk.Label(text="", bg='orange', font=('Nunito', 12), fg="red")
err1 = False

message_frame = tk.Frame(root)
message_label = tk.Label(message_frame, text="Mesaj:")

message_entry = tk.Entry(message_frame, width=45)
imagem = tk.PhotoImage(file="image-removebg-preview (3).png")
imagem = imagem.subsample(13, 13)
send_button = tk.Button(message_frame, image=imagem, command=send_message, border=0, width=40, height=40) 
a = 0

root.bind('<Destroy>', on_close)

root.mainloop()
