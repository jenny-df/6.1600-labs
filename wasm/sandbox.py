import pywasm
import wasi

def sha256(v):
    wasimod = wasi.Wasi(['sha-export.wasm'])
    runtime = pywasm.load('sha-export.wasm', { 'wasi_snapshot_preview1': wasimod.imports() })

    # Using malloc to get permitted locations to store data according to sandbox
    d = runtime.exec("malloc", (len(v),)) 
    n = len(v)
    num_sha256_bytes = 256//8
    md = runtime.exec("malloc", (num_sha256_bytes,)) 

    first_memory_inst_in_store = runtime.store.memory_list[0].data

    first_memory_inst_in_store[d:d + n] = v
    runtime.exec('SHA256', (d, n, md))
    return bytes(first_memory_inst_in_store[md:md+num_sha256_bytes])
