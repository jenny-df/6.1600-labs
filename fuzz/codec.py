import string

printable = string.printable[:94].encode('ascii')
alphanumeric = (string.ascii_letters + string.digits).encode('ascii')
printable_not_alphanumeric_or_and = bytes(c for c in printable if c not in alphanumeric and bytes([c]) != b'&')

encoding = {}
decoding = {}
k, j, i_val = 0, 0, bytes([printable_not_alphanumeric_or_and[0]])

for i in range(256):
    inp = bytes([i])
    if inp in alphanumeric:
        encoding[i] = inp
    else:
        output = b'&' + i_val + bytes([printable_not_alphanumeric_or_and[j]])
        encoding[i] = output
        decoding[output] = inp

        if j < len(printable_not_alphanumeric_or_and)-1:
            j += 1
        else:
            k += 1
            j, i_val = 0, bytes([printable_not_alphanumeric_or_and[k]])
# Requirements:
#
# - Your codec must encode bytes into bytes, and decode back into bytes.
# - Your codec must encode arbitrary bytes.  It must be possible to
#   encode any byte sequence, and decode it correctly.
# - The encoding must be printable (every encoding byte must be in the
#   `printable` bytes object.  Your encodings cannot contain non-printable
#   bytes.
# - Alphanumeric inputs (where every character is in string.ascii_letters
#   or string.digits) must be encoded one-to-one: the encoding must be the
#   same as the input.
# - The encoding should be at most 3x the size of the input, in the worst case.
# - The encoding must be recoverable.  This means that, if you take an encoding
#   and chop off some parts of it (at the beginning or at the end), then decoding
#   that chopped part should produce the corresponding part of the original string,
#   modulo things that might have gotten cut off at each end.

def encode(input):
    encoded = b''
    for byte in input:
        encoded += encoding[byte]

    return encoded

def decode(buf):
    decoded = b''
    i = 0
    while i < len(buf):
        if bytes([buf[i]]) == b'&':
            if i + 2 >= len(buf):
                break
            decoded += decoding[buf[i:i+3]]
            i += 2
        elif bytes([buf[i]]) in alphanumeric:
            decoded += bytes([buf[i]])
        i += 1
    return decoded

def encode_and_decode(i):
    enc = encode(i)
    dec = decode(enc)
    print(i, "->", enc, "->", dec)

if __name__ == "__main__":
    encode_and_decode(b"hello world")
    encode_and_decode(b"\x00\x01\x02\x03")
