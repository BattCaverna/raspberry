import SocketServer
import inspect
import sipo
import time

class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            self.request.sendall("> ")
            line = self.rfile.readline()
            if line == "":
                break
            data = line.strip().split()
            if len(data) > 0:
                cmd = data[0]
                for command in inspect.getmembers(self, predicate=inspect.ismethod):
                    if command[0] == "cmd_" + cmd:
                        stop = command[1](data)
                        self.request.sendall("\n")
                        if stop == True:
                            return
                        break
                else:
                    self.request.sendall("-1 Command not found.\n\n")

    def cmd_pulseoutcond(self, args):
        try:
            out = int(args[1])
            val = int(args[2])
            delay = int(args[3])
            cond = int(args[4])
        except:
            self.request.sendall("-2 Invalid arguments.\n")
            return

        inp = sipo.getinput(cond)
        if bool(val) != bool(inp):
            self.cmd_pulseout([None, out, True, delay])
        else:
            self.request.sendall("0 Command OK.\n")

    def cmd_pulseout(self, args):
        try:
            out = int(args[1])
            val = int(args[2])
            delay = int(args[3])
        except:
            self.request.sendall("-2 Invalid arguments.\n")
            return

        self.request.sendall("0 Command OK.\n")
        sipo.setout(out, val)
        time.sleep(delay/1000.0)
        sipo.setout(out, not val)

    def cmd_setout(self, args):
        try:
            out = int(args[1])
            val = int(args[2])
        except:
            self.request.sendall("-2 Invalid arguments.\n")
            return

        self.request.sendall("0 Command OK.\n")
        sipo.setout(out, val)
        
    def cmd_getout(self, args):
        try:
            out = int(args[1])
        except:
            self.request.sendall("-2 Invalid arguments.\n")
            return

        self.request.sendall("0 Command OK.\n")
        val = sipo.getout(out)
        if val:
            self.request.sendall("1\n")
        else:
            self.request.sendall("0\n")

    def cmd_getin(self, args):
        try:
            inp = int(args[1])
        except:
            self.request.sendall("-2 Invalid arguments.\n")
            return

        self.request.sendall("0 Command OK.\n")
        val = sipo.getinput(inp)
        if val:
            self.request.sendall("1\n")
        else:
            self.request.sendall("0\n")

    def cmd_getcachedin(self, args):
        try:
            inp = int(args[1])
        except:
            self.request.sendall("-2 Invalid arguments.\n")
            return

        self.request.sendall("0 Command OK.\n")
        val = sipo.getcachedinput(inp)
        if val:
            self.request.sendall("1\n")
        else:
            self.request.sendall("0\n")

    def cmd_quit(self, args):
        self.request.sendall("0 Bye Bye!\n")
        return True


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8023

    # Create the server
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    sipo.stop()
