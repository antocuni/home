import time

def bench(fn):
    def inner(*args, **kwds):
        start = time.clock()
        res = fn(*args, **kwds)
        end = time.clock()
        try:
            name = fn.__name__
        except AttributeError:
            name = repr(fn)
        #
        print '%s: %.2f seconds' % (name, end-start)
        return res
    return inner
