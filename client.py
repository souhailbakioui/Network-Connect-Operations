import socket
import tkinter as tk
from tkinter import messagebox



def connect_to_server():
    server_ip = ip_entry.get()
    server_port = int(port_entry.get())
    
    try:
        client_socket.connect((server_ip, server_port))
        print('Connected to the server')
        output_text.insert(tk.END, 'Connected to the server\n')
        
        client_socket.send(b'Welcome Sir')
        welcome_message = client_socket.recv(1024).decode()
        print(f'Server: {welcome_message}')
        output_text.insert(tk.END, f'Server : {welcome_message}, Your  IP Is : {server_ip} and Your Port : {server_port}\n')
        
        connect_button.config(state=tk.DISABLED)
        send_button.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Error", f"Connection error: {str(e)}")


def send_request():
    a = value_a_entry.get()
    b = value_b_entry.get()
    operator = operator_entry.get()

    if operator not in ['+', '-', '*', '/']:
        messagebox.showerror("Error", "Invalid operator. Please enter +, -, *, or /.")
        return

    request = f'CALC {a} {b} {operator}'
    client_socket.sendall(request.encode())

    if request == 'CALC FIN':
        bye_message = client_socket.recv(1024).decode()
        print(f'Server : {bye_message}')
        output_text.insert(tk.END, f'Server : {bye_message}\n')
        client_socket.close()
        root.destroy()
    else:
        result = client_socket.recv(1024).decode()
        print(f'Server : {result}')
        output_text.insert(tk.END, f'Server : {result}\n')

    value_a_entry.delete(0, tk.END)
    value_b_entry.delete(0, tk.END)
    operator_entry.delete(0, tk.END)


def close_connection():
    client_socket.sendall('Closed'.encode())
    bye_message = client_socket.recv(1024).decode()
    print(f'Server : {bye_message}')
    output_text.insert(tk.END, f'Server : {bye_message}\n')
    client_socket.close()
    root.destroy()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
textColor="#333333"
bgColor="#cfe7e8"
root = tk.Tk()
root.title('Network Connect Operations')
root.configure(bg=bgColor)
# Server IP
ip_label = tk.Label(root, text="Server IP:", fg=textColor,bg=bgColor, font=("Arial", 12, "bold"))
ip_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
ip_entry = tk.Entry(root, font=("Arial", 12))
ip_entry.grid(row=0, column=1, padx=10, pady=10)
ip_entry.insert(0, "localhost")
root.iconbitmap("Images\connection.ico")


# Server Port
port_label = tk.Label(root, text="Server Port:", fg=textColor ,bg=bgColor, font=("Arial", 12, "bold"))
port_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
port_entry = tk.Entry(root, font=("Arial", 12))
port_entry.grid(row=1, column=1, padx=10, pady=10)
port_entry.insert(0, "8888")

# Connect Button
connect_button = tk.Button(root, text="Connect", fg="green", font=("Arial", 12, "bold"), command=connect_to_server)
connect_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Value A
value_a_label = tk.Label(root, text="Value A:", fg=textColor,bg=bgColor, font=("Arial", 12, "bold"))
value_a_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
value_a_entry = tk.Entry(root, font=("Arial", 12))
value_a_entry.grid(row=3, column=1, padx=10, pady=10)

# Value B
value_b_label = tk.Label(root, text="Value B:", fg=textColor ,bg=bgColor, font=("Arial", 12, "bold"))
value_b_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
value_b_entry = tk.Entry(root, font=("Arial", 12))
value_b_entry.grid(row=4, column=1, padx=10, pady=10)

# Operator
operator_label = tk.Label(root, text="Operator (+, -, *, /):", fg=textColor ,bg=bgColor, font=("Arial", 12, "bold"))
operator_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
operator_entry = tk.Entry(root, font=("Arial", 12))
operator_entry.grid(row=5, column=1, padx=10, pady=10)

# Send Button
send_button = tk.Button(root, text="Send", fg="blue", font=("Arial", 12, "bold"), command=send_request)
send_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Close Connection Button
close_button = tk.Button(root, text="Close Connection", fg="red", font=("Arial", 12, "bold"), command=close_connection)
close_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Output Text
root.resizable(False, False)  # Disable window resizing
output_text = tk.Text(root, font=("Arial", 12), width=30, height=10)
output_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
