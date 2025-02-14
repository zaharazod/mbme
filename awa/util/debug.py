from pprint import pp

DEBUG = 0


def debug(*args, level=DEBUG, **kwargs):
    if level == DEBUG:
        for x in args + tuple(kwargs.items()):
            pp(x)


## veeery hacky but all i need right now
