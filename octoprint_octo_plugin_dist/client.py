import socket
from os.path import exists
import threading
import time
import json
class client():
    def __init__(self,plugin):
        self.__id = -1
        self.__plugin = plugin
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect(('192.168.1.107', 42069))
        print("Connected")
        self.__sock.setblocking(1)
        self.__sock.send(bytes("0\n", "utf-8"))
        if not exists("/home/pi/aux/pi_info.txt"):
            with open("/home/pi/aux/pi_info.txt", "w") as file:
                self.__sock.send(bytes("NEW_PI\n", "utf-8"))
                msg = self.__sock.recv(1024)
                file.write(msg.decode("utf-8"))
                self.__id = json.loads(msg.decode("utf-8"))["ID"]
        else:
            with open("/home/pi/aux/pi_info.txt", "r") as file:
                self.__sock.send(bytes("PI\n", "utf-8"))
                file_content = file.readlines()[0]
                self.__sock.send(bytes(file_content, "utf-8"))
                self.__id = json.loads(file_content)["ID"]
                print(self.__id)

        print("My id is:" + str(self.__id))

        listener = Listener(self.__sock,self.__plugin)
        print("Starting Listener!")
        listener.start()
        updater = Updater(self.__sock,self.__plugin,self.__id)
        print("Starting Updater!")
        updater.start()

    def shutDown(self):
        self.__sock.close()


class Listener(threading.Thread):
    def __init__(self,sock,plugin):
        threading.Thread.__init__(self)
        self.__sock = sock
        self.__plugin = plugin
    def run(self):
        while True:
            print("Awaiting request")
            req_len = int.from_bytes(self.__sock.recv(4), "big")
            req = self.__sock.recv(req_len)
            req_type = req.decode("utf-8")
            print(bytes(req_type,"utf-8"))
            if req_type == "ADD_GCODE":
                len = int.from_bytes(self.__sock.recv(4),"big")
                fileName = bytes.decode(self.__sock.recv(len),"utf-8");
                fileSize = int.from_bytes(self.__sock.recv(4),"big")
                file = self.__sock.recv(fileSize,socket.MSG_WAITALL)
                print("Filename length:" + str(len))
                print("Filename:" + fileName)
                print("File length:" + str(fileSize))
                with open("/home/pi/.octoprint/uploads/" +fileName,"wb") as binary_file:
                    binary_file.write(file)
                    binary_file.close()
                    self.__plugin._printer.select_file("/home/pi/.octoprint/uploads/" +fileName, False, tags={"printscheduler"})
                    self.__plugin._printer.start_print(tags={"printscheduler"})
            elif req_type == "HOME":
                print("Goin home!")
                self.__plugin._printer.home(["x","y","z"])
            elif req_type == "MOVE":
                print("Movin'")
                len = int.from_bytes(self.__sock.recv(4),"big")
                move_data = bytes.decode(self.__sock.recv(len),"utf-8");
                self.__plugin._printer.jog(json.loads(move_data))
            elif req_type == "SET_TEMP":
                print("Temperature!")
                len = int.from_bytes(self.__sock.recv(4),"big")
                temp_target = bytes.decode(self.__sock.recv(len),"utf-8")
                temp = int.from_bytes(self.__sock.recv(4),"big")
                self.__plugin._printer.set_temperature(temp_target,temp)
            elif req_type == "SET_TEMP_OFFSET":
                print("Temperature offset!")
                len = int.from_bytes(self.__sock.recv(4),"big")
                offset = bytes.decode(self.__sock.recv(len),"utf-8")
                self.__plugin._printer.set_temperature_offset(json.loads(offset))



class Updater(threading.Thread):
    def __init__(self,sock,plugin,id):

        threading.Thread.__init__(self)
        self.__sock = sock
        self.__plugin = plugin
        self.__id = id


    def run(self):
            while True:
                connection = self.__plugin._printer.get_current_connection()
                temperatues = self.__plugin._printer.get_current_temperatures()
                job = self.__plugin._printer.get_current_job()
                operational = self.__plugin._printer.is_operational()
                pause = self.__plugin._printer.is_paused()
                pausing = self.__plugin._printer.is_pausing()
                printing = self.__plugin._printer.is_printing()
                ready = self.__plugin._printer.is_ready()
                status = json.dumps({
                    "connection": connection,
                    "temps": temperatues,
                    "job": job,
                    "operational": operational,
                    "pause": pause,
                    "pausing":pausing,
                    "printing":printing,
                    "ready":ready
                })
                self.__sock.send(bytes("UPDATE\n","utf-8"))
                self.__sock.send(bytes(str(self.__id)+"\n","utf-8"))
                self.__sock.send(bytes(str(status)+"\n","utf-8"))
                print(status)
                time.sleep(5)
