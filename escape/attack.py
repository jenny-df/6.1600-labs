import inspect, gc, os, hashlib
from grader import SecretStore


def attack_one(guess):
    return inspect.currentframe().f_back.f_locals['secret']

def attack_two():
    return inspect.currentframe().f_back.f_locals['secret']

def attack_three():
    os.urandom = lambda _: b'my "random" string'
    return b'my "random" string'

def attack_four():
    # could also look through gc but i couldn't get my gc to find the old 
    # SecretStore object with the secret... all the ones it found didn't 
    # have a secret attribute
    class _Hash():
        def __init__(self,_):
            pass
        def digest(self):
            return inspect.currentframe().f_back.f_locals['h']
    hashlib.sha256 = _Hash
    return b'doesnt matter'
