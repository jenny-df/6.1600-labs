from arc4 import ARC4

import zlib

class Attacker:
    def __init__(self, v):
        self.victim = v

    def attack_one(self, plaintext, ciphertext, attack_msg):
        # You may NOT use self.victim, since this is
        # a passive attack.
        iv = ciphertext[:3]
        ct = ciphertext[3:]

        plaintext_hash = zlib.crc32(plaintext).to_bytes(4, 'big')
        attack_msg_hash = zlib.crc32(attack_msg).to_bytes(4, 'big')

        key = bytes(a ^ b for a, b in zip(ct, plaintext+plaintext_hash))
        attack = bytes(a ^ b for a, b in zip(key, attack_msg+attack_msg_hash))
  
        return iv+attack

    def attack_two(self, ciphertext, attack_msg):
        # You may NOT use self.victim, since this is
        # a passive attack.

        iv = ciphertext[:3]
        ct = ciphertext[3:]

        attack_msg_hash = zlib.crc32(attack_msg).to_bytes(4, 'big')
        zero = b'\x00'*256
        zero_hash = zlib.crc32(zero).to_bytes(4, 'big')

        attack = bytes(a ^ b ^ c for a, b, c in zip(ct, attack_msg + attack_msg_hash, zero + zero_hash))

        return iv + attack

    def attack_three(self, target):
        # You may NOT call self.victim.send_packet() 
        # or self.victim.receive_packet() here.
        #
        # You may call self.victim.check_packet(),
        # defined in grader.py.
        
        ### Your cleverness here
        return None
