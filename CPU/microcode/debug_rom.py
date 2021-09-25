import yaml, os
from opcode import opcode

def cv(opc):
    x = [ord(c) for c in opc]
    result = ""
    for y in x:
        result = result + f'{y:08b}'
    return int(result, 2)

OPCODES = []

# Read in all the Opcodes and add them to the global list
FILEPATH = "./opcodes"

# Find all the opcode YAML files
filenames = []
for root, dirs, files in os.walk(FILEPATH):
    for file in files:
        if file.lower().endswith("yaml".lower()):
            filenames.append(os.path.join(root, file))

MEMORY = []

for x in range(256):
    MEMORY.append(0)

for opfile in filenames:
    with open(opfile) as file:
        codes = yaml.load(file, Loader=yaml.FullLoader)
    #print(f"Loading Opcodes for file {opfile}")
    for item in codes:
        #print(f"--- Loading Opcode { item }")
        OPCODES.append(opcode(item, **codes[item]))

for x in OPCODES:
    MEMORY[x.code] = cv(x.syntax[:3])

with open('opcodes.bin', 'wb') as out_file:
    for x in MEMORY:
        out_file.write(x.to_bytes(3, 'little'))
