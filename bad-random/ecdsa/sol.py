import time
from datetime import datetime
import hashlib
from ecdsa import SigningKey, NIST256p

def problem_1a(date_string, public_key):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    total_seconds = int(date_object.timestamp())
    SECONDS_IN_DAY = 24*60*60

    for time in range(total_seconds, total_seconds+SECONDS_IN_DAY):
        b_retrieved = b'%d' % time
        h_retrieved = hashlib.sha256(b_retrieved).digest()
        secexp = int.from_bytes(h_retrieved, "big")
        sk = SigningKey.from_secret_exponent(secexp, curve=NIST256p)
        vk = sk.verifying_key

        if vk == public_key:
            return sk
    return None # FAILURE

def problem_2b(sig1, sig2, Hm1, Hm2):
    q = 6277101735386680763835789423176059013767194773182842284081
    a_t = (Hm1 - Hm2) * pow(sig1[1] - sig2[1], -1, q) % q
    a = (sig1[1] * a_t - Hm1) * pow(sig1[0], -1, q) % q
    return a
