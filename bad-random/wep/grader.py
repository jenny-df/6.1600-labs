import os
import traceback

from attacker import Attacker
from victim import Victim

def grade_one():
    v = Victim()
    plaintext = os.urandom(256)
    ciphertext = v.send_packet(plaintext)
    attack_msg = os.urandom(256)

    a = Attacker(None)
    
    packet = a.attack_one(plaintext, ciphertext, attack_msg)

    msg = v.receive_packet(packet)
    if msg is None:
        raise Exception("Victim rejected packet")
    if msg != attack_msg:
        raise Exception("Forged message is incorrect")

def grade_two():
    v = Victim()
    plaintext = os.urandom(256)
    ciphertext = v.send_packet(plaintext)
    attack_xor = os.urandom(256)
    expected = bytes([plaintext[i] ^ attack_xor[i] for i in range(256)])

    a = Attacker(None)
    packet = a.attack_two(ciphertext, attack_xor)
    msg = v.receive_packet(packet)
    if msg is None:
        raise Exception("Victim rejected packet")
    if msg != expected:
        print(msg,"\n", expected)
        raise Exception("Forged message is incorrect")

def grade_three():
    v = Victim()

    plaintext = os.urandom(256)
    target_packet = v.send_packet(plaintext)
    f = v.receive_packet
    v.send_packet = None
    v.receive_packet = None

    # Returns the bit of whether victim accepted packet
    def check_packet(packet):
        return f(packet) != None
    v.check_packet = check_packet

    a = Attacker(v)
    key = bytes(a ^ b for a, b in zip(target_packet[3:-4], plaintext))
    # key = bytes(a ^ b for a, b in zip(key, plaintext))
    guess = a.attack_three(target_packet)

    if plaintext != guess:
        raise Exception("Incorrect guess")

checks = {
    "one": grade_one,
    "two": grade_two,
    "three": grade_three,
}

if __name__ == '__main__':
    for n, f in checks.items():
        try:
            f()
            print("%s: pass" % n)
        except:
            traceback.print_exc()
            print("%s: fail" % n)
