import numpy as np
import yaml, os
from opcode import opcode

FILEPATH = "./opcodes"
ROM_SIZE = 131071
BASE_CW = 0

# Find all the opcode YAML files
filenames = []
for root, dirs, files in os.walk(FILEPATH):
    for file in files:
        if file.lower().endswith("yaml".lower()):
            filenames.append(os.path.join(root, file))

# Build a list of opcode() objects
OPCODES = []            
for opfile in filenames:
    with open(opfile) as file:
        codes = yaml.load(file, Loader=yaml.FullLoader)
    print(f"Loading Opcodes for file {opfile}")
    for item in codes:
        #print(f"--- Loading Opcode { item }")  ## Useful for debugging bad micocode
        OPCODES.append(opcode(item, **codes[item]))

def bitcheck(n, k):
    """function to check whether the bit at given position is set or unset"""
    new_num = n >> (k - 1)
    #if it results to '1' then bit is set,
    return (new_num & 1)

MEMORY = []

for x in range(ROM_SIZE):          # Creates our ROM object full of base control words
    MEMORY.append(np.uint32(BASE_CW))

def get_step_addresses(base, step):
    """Given a base byte and the step this function returns a list of addresses in the memory range"""
    base = int(base)
    result = []
    for x in range(32):
        result.append((x << 11) |  ( step << 8 ) | base)

    return result

for opcode in OPCODES:
    c = 0
    for step in opcode.steps:
        #print(f"Working on {opcode.syntax}, the steps look like {opcode.steps}")
        if 'all' in step:
            for address in get_step_addresses(opcode.code, c):
                MEMORY[address] = step['all']
        if 'c_set' in step:
            for address in get_step_addresses(opcode.code, c):
                if bitcheck(address, 15):
                    MEMORY[address] = step['c_set']
                else:
                    MEMORY[address] = step['c_unset']
        if 'z_set' in step:
            for address in get_step_addresses(opcode.code, c):
                if bitcheck(address, 14):
                    MEMORY[address] = step['z_set']
                else:
                    MEMORY[address] = step['z_unset']
        if 'n_set' in step:
            for address in get_step_addresses(opcode.code, c):
                if bitcheck(address, 13):
                    MEMORY[address] = step['n_set']
                else:
                    MEMORY[address] = step['n_unset']
        if 'v_set' in step:
            for address in get_step_addresses(opcode.code, c):
                if bitcheck(address, 12):
                    MEMORY[address] = step['v_set']
                else:
                    MEMORY[address] = step['v_unset']
        if 'a_set' in step:
            for address in get_step_addresses(opcode.code, c):
                if bitcheck(address, 16):
                    MEMORY[address] = step['a_set']
                else:
                    MEMORY[address] = step['a_unset']

        c = c + 1

# ---------------------------- #
# Finalize ROMS                #
# ---------------------------- #
rom0 = bytearray()
rom1 = bytearray()
rom2 = bytearray()
rom3 = bytearray()

for x in MEMORY:
    numbers = list((x >> i) & 0xFF for i in range(0,32,8))
    rom0.append(numbers[0])
    rom1.append(numbers[1])
    rom2.append(numbers[2])
    rom3.append(numbers[3])

with open('rom0.bin', 'wb') as out_file:
    out_file.write(rom0)

with open('rom1.bin', 'wb') as out_file:
    out_file.write(rom1)

with open('rom2.bin', 'wb') as out_file:
    out_file.write(rom2)

with open('rom3.bin', 'wb') as out_file:
    out_file.write(rom3)
