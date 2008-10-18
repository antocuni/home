#!/usr/bin/env python

try:
    import sys, os, termios
except ImportError:
    # on top of PyPy
    def ask_for_information(query, answer_last_chars, callback):
        raise OSError
else:
    def ask_for_information(query, answer_last_chars, callback):
        ttyname = os.ttyname(sys.stdout.fileno())
        freply = open(ttyname, 'rb')
        fd = freply.fileno()

        old = termios.tcgetattr(fd)     # a copy to save
        new = old[:]

        new[3] = new[3] & ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, new)

            sys.stdout.write(query)
            sys.stdout.flush()
            while True:
                reply = []
                p = None
                while p is None or reply[-1] not in answer_last_chars:
                    ch = freply.read(1)
                    if ch == '\033':
                        p = len(reply)
                    reply.append(ch)
                if callback(''.join(reply[p+1:])):
                    break

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        freply.close()

RXVT_TERMINAL = False

def detect_rxvt_terminal():
    if not hasattr(sys.stdout, 'fileno'):
        return
    def callback(reply):
        if reply.endswith('z'):
            global RXVT_TERMINAL
            RXVT_TERMINAL = True
            return False
        return True
    try:
        ask_for_information('\033[2z\033[5n', 'zn', callback)
    except (IOError, OSError):
        pass

if __name__ == '__main__':
    detect_rxvt_terminal()
    sys.exit(not RXVT_TERMINAL)
