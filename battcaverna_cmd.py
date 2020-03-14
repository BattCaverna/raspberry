import SocketServer
import inspect
import sipo
import time

class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        reply = ""
        while True:
            line = self.rfile.readline()
            if line == "":
                break
            data = line.strip().split()
            if len(data) > 0:
                cmd = data[0]
                for command in inspect.getmembers(self, predicate=inspect.ismethod):
                    if command[0] == "cmd_" + cmd:
                        ret = command[1](data)
                        if ret is None:
                            return
                        elif ret[0] == 0:
                            reply = "0 Command OK.%s%s" % ("\n" if len(ret) > 1 else "", "\n".join(ret[1:]))
                        elif ret[0] == -2:
                            reply = "-2 Invalid arguments."
                        else:
                            reply = "%d Error.%s" % "\n".join(ret[1:])
                        break
                else:
                    reply = "-1 Command not found."
            else:
                reply = ""

            self.request.sendall("%s\n" % reply)

    def cmd_pulseoutcond(self, args):
        try:
            out = int(args[1])
            val = int(args[2])
            delay = int(args[3])
            cond = int(args[4])
        except:
            return [-2]

        inp = sipo.getinput(cond)
        if bool(val) != bool(inp):
            return self.cmd_pulseout(["", out, 1, delay])
        return [0]

    def cmd_pulseout(self, args):
        try:
            out = int(args[1])
            val = int(args[2])
            delay = int(args[3])
        except:
            return [-2]

        sipo.setout(out, val)
        time.sleep(delay/1000.0)
        sipo.setout(out, not val)
        return [0]

    def cmd_setout(self, args):
        try:
            out = int(args[1])
            val = int(args[2])
        except:
            return [-2]

        sipo.setout(out, val)
        return [0]

    def cmd_getout(self, args):
        try:
            out = int(args[1])
        except:
            return [-2]

        val = sipo.getout(out)
        ret = [0]
        ret.append("1" if val else "0")
        return ret

    def cmd_getin(self, args):
        try:
            inp = int(args[1])
        except:
            return [-2]

        val = sipo.getinput(inp)
        ret = [0]
        ret.append("1" if val else "0")
        return ret

    def cmd_getcachedin(self, args):
        try:
            inp = int(args[1])
        except:
            return [-2]

        val = sipo.getcachedinput(inp)
        ret = [0]
        ret.append("1" if val else "0")
        return ret

    def cmd_quit(self, args):
        self.request.sendall("0 Bye Bye!\n")


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8023

    # Create the server
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    sipo.stop()
