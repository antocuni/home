import xchat
__module_name__ = "fijalcolor"
__module_version__ = "0.1" 
__module_description__ = "change the nick color of fijal because it's the same as arigato"

def check_message(word, word_eol, userdata):
    nick = word[0]
    line = word[1]
    if nick == '\x0326fijal':
        nick = ' fijal'
        xchat.emit_print("Channel Message", nick, line)
        return xchat.EAT_XCHAT
    
xchat.hook_print("Channel Message", check_message, "mydata")

print "\0034",__module_name__, __module_version__,"has been loaded\003"
