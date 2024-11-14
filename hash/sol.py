from hashall import *
from hashbig import *
import json, string, random

# return password, where toy_hash(password) = 80239fad1247
def problem_2a():
    target = "80239fad1247"
    with open('words_dict.json', 'r') as file:
        eng_words = json.load(file)

    for word in eng_words.keys():
        word = word.encode("ascii")
        if toy_hash(word).hex() == target:
            return word
    return None

# return password, where toy_hash(password) is in hashes.txt
def problem_2c():
    hashed_passwords = set()
    with open('hashes.txt', 'r') as f:
        for hash_ in f:
            hashed_passwords.add(hash_.strip())

    while True:
        password = ""
        for _ in range(20):
            password += random.choice(string.ascii_letters)
        hashed_pass = toy_hash(password.encode("ascii")).hex()
        if hashed_pass in hashed_passwords:
            return password

# return probability of being in bin k
def problem_3a(B, N):
    prob = 1/N
    return prob

# return probability of both balls being in bin k
def problem_3b(B,N):
    prob = 1/N**2
    return prob

# return number of ball pairs
def problem_3c(B):
    return ((B-1) * B)/2

# return reasonable upper bound
def problem_3d(B,N):
    num_pairs = problem_3c(B)
    prob_2_into_bin_k = problem_3b(B,N)
    prob_2_into_any_bin = N * prob_2_into_bin_k
    prob = prob_2_into_any_bin * num_pairs
    return prob
    
# return reasonable upper bound
def problem_3e(L,N):
    prob = problem_3d(L,2**N)
    return prob

# return h1,h2 where H(h1) == H(h2)
def problem_4b():
    data = "hi".encode('utf-8')
    h1, h2 = H(h1), H(H(h2))

    # Finding the cycle
    while h1 != h2:
        h1, h2 = H(h1), H(H(h2))

    # Finding the start of the cycle (the only point where a collision
    # with different values occurs)
    h1 = data # reset the first var/pointer
    while h1 != h2:
        prev1, prev2 = h1, h2
        h1, h2 = H(h1), H(h2)
    return prev1, prev2
