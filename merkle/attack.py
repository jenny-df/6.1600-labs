from random import randbytes
from common import Proof, H_kv, traversal_path

class AttackOne:
    def __init__(self, s):
        self._store = s

    def attack_fake_key(self):
        self._store.reset()
        self._store.insert(b"hell", b"oworld")
        return b'hell'

    def lookup(self, key):
        return self._store.lookup(key)

class AttackTwo:
    def __init__(self, s):
        self._store = s
        self.keys_vals = {}
        self.done = False

    def attack_fake_keys(self):
        return self.keys_vals

    def attack_key_value(self):
        self._store.reset()
        while len(self.keys_vals) < 1000:
            key = randbytes(5)
            val = randbytes(5)
            if key not in self.keys_vals:
                self.keys_vals[key] = val
                self._store.insert(key, val)

        self.children1_hash = self._store.root._children[0]._hashval
        self.children2_hash = self._store.root._children[1]._hashval
        self._store.reset()
        return self.children1_hash, self.children2_hash

    def lookup(self, key):
        if not self.done:
            self._store.reset()
            for k, v in self.keys_vals.items():
                self._store.insert(k, v)
            self.done = True
        return self._store.lookup(key)

class AttackThree:
    def __init__(self, s):
        self._store = s

    def lookup(self, key):
        children = self._store.root._children
        hash_ = children[0]._hashval + children[1]._hashval
        return Proof(None, None, [hash_])

class AttackFour:
    def __init__(self, s):
        self._store = s
        self.hash = b''
        self.attack_key_so_far = b''

    def insert(self, key, val):
        key_val_hash = H_kv(key, val)
        general_proof = Proof(None, None, [])

        if self.attack_key_so_far == b'':
            self.attack_key_so_far = key + val
        else:
            general_proof.siblings.append(self.attack_key_so_far)

            if traversal_path(key)[0]:
                self.attack_key_so_far = self.attack_key_so_far + key_val_hash
            else:
                self.attack_key_so_far = key_val_hash + self.attack_key_so_far

        return general_proof

    def attack_fake_key(self):
        return self.attack_key_so_far

    def lookup(self, key):
        return Proof(self.attack_key_so_far, b'', [])
