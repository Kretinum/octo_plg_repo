import socket
from os.path import exists
import threading

class client():
    def __init__(self,plugin):
        self.__plugin = plugin
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect(('192.168.1.104', 42069))
        print("Connected")
        self.__sock.setblocking(1)
        self.__sock.send(bytes("0\n", "utf-8"))
        if not exists("/home/pi/aux/pi_info.txt"):
            with open("/home/pi/aux/pi_info.txt", "w") as file:
                self.__sock.send(bytes("NEW_PI\n", "utf-8"))
                msg = self.__sock.recv(1024)
                file.write(msg.decode("utf-8"))
        else:
            with open("/home/pi/aux/pi_info.txt", "r") as file:
                self.__sock.send(bytes("PI\n", "utf-8"))
                self.__sock.send(bytes(file.readlines()[0], "utf-8"))

        threading.Thread(target=self.listen()).run()


    def listen(self):
        while True:
            self.__plugin._logger.info("Awaiting request")
            req = self.__sock.recv(1024)
            req_type = req.decode("utf-8")
            self.__plugin._logger.info(bytes(req_type,"utf-8"))
            self.__plugin._logger.info(req_type == "ADD_GCODE\r\n")
            if req_type == "ADD_GCODE\r\n":
                len = int.from_bytes(self.__sock.recv(4),"big")
                fileName = bytes.decode(self.__sock.recv(len),"utf-8")
                fileSize = int.from_bytes(self.__sock.recv(4),"big")
                file = self.__sock.recv(fileSize)
                print("Filename length:" + str(len))
                print("Filename:" + fileName)
                print("File length:" + str(fileSize))
                with open("/home/pi/.octoprint/uploads/" + fileName,"wb") as binary_file:
                    binary_file.write(file)
