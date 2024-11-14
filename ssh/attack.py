import zlib

COUNTRIES = []
with open("capitals.txt", "r") as f:
    for line in f:
        COUNTRIES.append('": "' + line.strip() + '",\n')

def rand_country_generator(select_countries):
    for i, (_, _, c1) in enumerate(select_countries):
        for j, (_, _, c2) in enumerate(select_countries):
            if j != i:
                for k, (_, _, c3) in enumerate(select_countries):
                    if j != k and i != k:
                        yield '{\n"city0%s"city1%s"city2%s}\n' % (c1, c2, c3)

class AttackTamper:
    def __init__(self, compress):
        # compress (boolean) is set for the last extra credit part
        self.compress = compress
        self.bytes = 0
        self.num_data_packets = 0
 
    def handle_data(self, data):
        # change ls ./files/* to rm -r /
        # MAC that always outputs a 160-bit string of zeros. 
        if self.num_data_packets == 9:
            # Relevant data
            if self.compress:
                compressor = zlib.compressobj()

                compressor.compress(b'^\x00\x00\x00\x00\x00\x00\x00\rls ./files/*\n')
                current_data = compressor.flush(zlib.Z_FULL_FLUSH)
                current_data = current_data.rjust(5 + len(current_data), b'\x00')

                compressor.compress(b'^\x00\x00\x00\x00\x00\x00\x00\rrm -r /\n')
                final_data = compressor.flush(zlib.Z_FULL_FLUSH)
                final_data = final_data.rjust(5 + len(final_data), b'\x00')

                # Reduce the size of current data
                current_data = current_data[:len(final_data)]

            else:
                current_data = bytes("ls ./files/*\n", "utf-8")
                final_data = bytes("rm -r /\n", "utf-8")

                # Add a left 0s padding to both (which normally contains 
                # header and padding info)
                current_data = current_data.rjust(14 + len(current_data), b'\x00')
                final_data = final_data.rjust(14 + len(final_data), b'\x00')

            # Add right 0s padding to both (just padding in original + 
            # so that the final data is the same len as current data)
            current_data = current_data.ljust(len(data), b'\x00')
            final_data = final_data.ljust(len(data), b'\x00')

            # XOR all data to remove current data and add final data and 
            # add padding so that it's 160-bits long (i.e. it needs 20 bytes)
            data = bytes((i ^ j ^ k) for i, j, k in zip(data, current_data, final_data))

        self.num_data_packets += 1
        return data

def attack_decrypt(client_fn):
    # Data obtained from every country
    one_country_tests = []
    for country in COUNTRIES:
        output = client_fn(country + '"')
        one_country_tests.append(output+(country,))
    one_country_tests.sort(key=lambda x:x[0])

    # Only data that has minimum number of bytes
    min_out_bytes = one_country_tests[0][0]
    for i, vals in enumerate(one_country_tests):
        if vals[0] != min_out_bytes:
            if i <= 2:
                min_out_bytes = one_country_tests[i][0]
            else:
                break
    
    one_country_tests = one_country_tests[:i]

    # Combos of 3 possible countries
    three_country_tests = []
    for final_string in rand_country_generator(one_country_tests):
        output = client_fn(final_string)
        three_country_tests.append(output+(final_string,))
    three_country_tests.sort(key=lambda x:(x[0], x[1]))

    return three_country_tests[0][2]

