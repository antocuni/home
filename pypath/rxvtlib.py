def metadata(text, flag):
    return '\033[1;%d;%dz%s' % (len(text), flag, text.encode('hex'))

metadata_stop = '\033[0z'

def format_command(text, command, force=False):
    pieces = [text]
    if RXVT_TERMINAL or force:
        buffer = metadata(command, 4)
        pieces.insert(0, buffer)
        pieces.append(metadata_stop)
    return ''.join(pieces)

def command_in_term(cmd, title=None, pause=False, term='rxvt'):
    if title is not None:
        title = '-title %s' % title
    else:
        title = ''
    cmd = cmd.replace('"', r'\"')
    if pause:
        cmd += '; read'
    res = '%s %s -e bash -c "%s" &' % (term, title, cmd)
    return res

def openfile_format(text, filename, lineno):
    filename = filename.replace("'", "\\'")
    command = "e +%s '%s'" % (lineno, filename)
    return format_command(text, command)

def get_terminal_size():
    try:
        import termios, fcntl, struct
        call = fcntl.ioctl(0, termios.TIOCGWINSZ, "\x00"*8)
        height, width = struct.unpack("hhhh", call)[:2]
    except (SystemExit, KeyboardInterrupt), e:
        raise
    except:
        width = int(os.environ.get('COLUMNS', 80))
        height = int(os.environ.get('COLUMNS', 24))
    return width, height

# ____________________________________________________________

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

detect_rxvt_terminal()   # eagerly, before stdout capturing
