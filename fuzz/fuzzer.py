import atheris
import sys
import msgpack

import msgpacker
import codec

import logging
logging.basicConfig(
    filename="fuzzing_log.txt",
    level=logging.DEBUG,
    format="%(message)s",
) 

def fuzzing_msg_packer(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    enc = msgpacker.encoder()
    fuzz_type = fdp.ConsumeIntInRange(0, 6)

    if fuzz_type == 0: # int
        val = fdp.ConsumeInt(8)
    elif fuzz_type == 1: # str
        val = fdp.ConsumeUnicodeNoSurrogates(50)
    elif fuzz_type == 2: # bytes
        val = fdp.ConsumeBytes(50)
    elif fuzz_type == 3: # dict
        val = {fdp.ConsumeUnicodeNoSurrogates(10): fdp.ConsumeUnicodeNoSurrogates(10) for _ in range(5)}
    elif fuzz_type == 4: # list
        val = [fdp.ConsumeUnicodeNoSurrogates(10) for _ in range(5)]
    elif fuzz_type == 5: # bool
        val = fdp.ConsumeIntInRange(0, 1) == 1
    else: # none
        val = None

    try:
        enc.encode(val)
        res = enc.get_buf()
        dec = msgpacker.decoder(res)
        decoded_data = dec.decode()

        good_packed = msgpack.packb(val)
        good_decoded_data = msgpack.unpackb(good_packed)
        if good_packed != res:
            raise msgpacker.BadEncodingException(f"PACKING {val}:\n     GOOD:{good_packed} \n     BAD:{res}\n\n")
        
        if good_decoded_data != decoded_data:
            raise msgpacker.BadEncodingException(f"UNPACKING {val}:\n     GOOD:{good_decoded_data} \n     BAD:{decoded_data}")
        
    except Exception as e:
        logging.debug(f"Input value: {val} with err msg: {e}")


def fuzzing_codec(data):
    fdp = atheris.FuzzedDataProvider(data)
    rand_len = fdp.ConsumeIntInRange(1, 100)
    val = fdp.ConsumeBytes(rand_len)

    try:
        enc = codec.encode(val)
        dec = codec.decode(enc)
        assert val == dec, f"{val} doesn't encode and decode back to itself -> new val {dec}"

        rand_pos = fdp.ConsumeIntInRange(0, max(len(enc)-1, 0))
        enc_end_sub = enc[:rand_pos]
        dec_end_sub = codec.decode(enc_end_sub)
        assert dec_end_sub in val, f"{dec_end_sub} isn't a subset of {val}"

        enc_start_sub = enc[rand_pos:]
        dec_start_sub = codec.decode(enc_start_sub)
        assert dec_start_sub in val, f"{dec_start_sub} isn't a subset of {val}"

    except Exception as e:
        logging.debug(f"{val} -> {enc} -> {enc_end_sub} -> {e}")

if __name__ == "__main__":
    atheris.instrument_all()
    # atheris.Setup(sys.argv, fuzzing_msg_packer)
    atheris.Setup(sys.argv, fuzzing_codec)
    atheris.Fuzz()