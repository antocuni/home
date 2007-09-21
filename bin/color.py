def color(s, fg=1, bg=1):
    template = '\033[%02d;%02dm%s\033[00m'
    return template % (bg, fg, s)

RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
GRAY = 37
