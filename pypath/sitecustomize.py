import sys

def info(type, value, tb):
    isatty = hasattr(sys.stderr, 'isatty') and sys.stderr.isatty()    
    if (hasattr(sys, 'ps1') and 'pypy' not in sys.version) or not isatty or\
            str(value) == 'underlying C/C++ object has been deleted':
        # You are in interactive mode or don't have a tty-like
        # device, so call the default hook
        sys. __excepthook__(type, value, tb)
    else:
        import traceback, pdb
        # You are not in interactive mode; print the exception
        traceback.print_exception(type, value, tb)
        print
        # ... then star the debugger in post-mortem mode
        pdb.pm()


sys.excepthook = info

