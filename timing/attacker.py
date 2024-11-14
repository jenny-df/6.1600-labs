import bad_server
import api
import secrets
import time
from typing import Optional

NUM_POSSIBLE_BYTES = 2**8

class Client:
    def __init__(self, remote: bad_server.BadServer):
        self._remote = remote
        self.unique_hexes = set()

        while len(self.unique_hexes) < NUM_POSSIBLE_BYTES:
            cur_byte = secrets.token_hex(1)
            if cur_byte not in self.unique_hexes:
                self.unique_hexes.add(cur_byte)

    def steal_password (self, l: int) -> Optional[str]:
        password = ""

        while not self._remote.verify_password(api.VerifyRequest(password)).ret:
            password = ""
            max_time = (0, "")

            for _ in range(l):
                for cur_byte in self.unique_hexes:
                    req = api.VerifyRequest(password + cur_byte)

                    start = time.perf_counter()
                    self._remote.verify_password(req)
                    end = time.perf_counter()
                    duration = end-start
                    
                    if duration > max_time[0]:
                        max_time = (duration, cur_byte)

                password += max_time[1]

        return password

if __name__ == "__main__":
    passwd = '37a4e5bf847630173da7e6d19991bb8d'
    nbytes = len(passwd) // 2
    server = bad_server.BadServer(passwd)
    alice = Client(server)
    print(alice.steal_secret_token(nbytes))
