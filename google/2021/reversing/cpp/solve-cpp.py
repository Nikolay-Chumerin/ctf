#!/usr/bin/env python

import angr
import claripy

STDIN_FD = 0

program_path = "./cpp-decoded"
# use ghidra to find out addresses of the success/failure outputs
success_address = 0x00101c2b
failure_address = 0x00101c18
base_address = 0x00100000


flag_length = 27

proj = angr.Project(program_path, main_opts={"base_addr": base_address})
flag_chars = [claripy.BVS(f"flag_{i}", 8) for i in range(flag_length)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])

state = proj.factory.full_init_state(
    args=[program_path],
    add_options=angr.options.unicorn,
    stdin=flag,
)

for k in flag_chars:
    state.solver.add(k >= ord('!'))
    state.solver.add(k <= ord('~'))

simgr = proj.factory.simulation_manager(state)
simgr.explore(find=success_address, avoid=failure_address)

if (len(simgr.found) > 0):
    for found in simgr.found:
        print(found.posix.dumps(STDIN_FD))
else:
    print("Not found")
