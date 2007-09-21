#!/usr/bin/env python

import sys
from color import color, RED, YELLOW, GREEN, CYAN, MAGENTA

value_types = 'BCDFIJSZ'

def split_if(s, sep):
    if sep in s:
        return s.split(sep, 1)
    else:
        return s, ''

def format_type(t, col):
    if t in value_types:
        return color(t, MAGENTA)
    if '/' in t:
        parts = t.split('/')
        parts[-1] = color(parts[-1], col)
        t = '/'.join(parts)
    return t

def format_stack(stack):
    stack = stack.strip()
    num, stack = split_if(stack, ' ')
    num = color(num, YELLOW)
    types = stack.split(';')
    stack = '; '.join(format_type(t, GREEN) for t in types)
    return '%s %s' % (num, stack)

def format_op(op):
    op = op.strip()
    opcode, args = split_if(op, ' ')
    args = args.replace(';', '; ')
    args = [format_type(t, CYAN) for t in args.split()]
    args = ' '.join(args)
    opcode = color(opcode, RED)
    return '%s %s' % (opcode, args)

def main():
    for line in sys.stdin:
        if ':' in line:
            stack, op = line.split(':', 1)
            print format_stack(stack)
            print format_op(op)
            print

if __name__ == '__main__':
    main()
    #print format_stack('00107  Ljava/util/HashMap;Ljava/util/HashMap;I')
