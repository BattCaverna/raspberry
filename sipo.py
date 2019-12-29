import spidev
import threading
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000
spi.cshigh = True
n_out = 16

out_state = [0x00] * (n_out/8)
in_state = spi.xfer(list(out_state))
lock = threading.RLock()
stopthread = False

def setout(out, val):
    i = out / 8
    bit = out % 8
    with lock:
        if val:
            out_state[i] |= (1 << bit)
        else:
            out_state[i] &= ~(1 << bit)
        spi.xfer(list(out_state))

def getout(out):
    i = out / 8
    bit = out % 8
    with lock:
        return (out_state[i] & (1 << bit) != 0)

def getinput(inp):
    i = inp / 8
    bit = inp % 8
    with lock:
        read = spi.xfer(list(out_state))
    return (read[i] & (1 << bit) == 0)

def getcachedinput(inp):
    i = inp / 8
    bit = inp % 8
    with lock:
        read = list(in_state)
        in_state[i] |= 1 << bit
    return (read[i] & (1 << bit) == 0)

def _input_thread():
    while not stopthread:
        with lock:
            read = spi.xfer(list(out_state))
            for i, r in enumerate(read):
                in_state[i] &= r
        time.sleep(0.1)

def stop():
    stopthread = True
    
x = threading.Thread(target=_input_thread)
x.daemon = True
x.start()
