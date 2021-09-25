import numpy as np
import ports as port
"""
ALUx Function Codes:
00000 - NOP
11010 - ADD
10101 - SUB
01000 - AND
01110 - OR
00110 - XOR
11100 - SHR
01010 - LHPASS
"""

CONTROLS = {
    'BASE': np.uint32(0),     # 00000000 - 00000000 - 00000000 - 00000000

    # ALU Operations
    'LH_PASS': np.uint32(1 << port.ALU_OE0 | 1 << port.ALU_OE1 ),
    'RH_PASS': np.uint32(1 << port.ALU_OE2),
    'ALU_OUT': np.uint32(1 << port.ALU_OE0),
    'ALU_SHR_OUT': np.uint32(1 << port.ALU_OE1),
    'ALU_ADD': np.uint32(1 << port.ALU_OP4 | 1 << port.ALU_OP3 | 1 << port.ALU_OP1 ),
    'ALU_SUB': np.uint32(1 << port.ALU_OP4 | 1 << port.ALU_OP2 | 1 << port.ALU_OP0 ),
    'ALU_SHR': np.uint32(1 << port.ALU_OE1),
    'ALU_AND': np.uint32(1 << port.ALU_OP3 ),
    'ALU_OR': np.uint32(1 << port.ALU_OP3 | 1 << port.ALU_OP2 | 1 << port.ALU_OP1  ),
    'CIN': np.uint32(1 << port.C_SEL1),
    'ZCIN': np.uint32(1 << port.C_SEL0),
    'ICIN': np.uint32(1 << port.C_SEL0 | 1 << port.C_SEL1),

    ## PC Register Operations
    'PC_INC': np.uint32(1 << port.MB_INC1),
    'PC_OUT': np.uint32(1 << port.MB_OE1),
    'PC_LDH': np.uint32(1 << port.DB_LD2),
    'PC_LDL': np.uint32(1 << port.DB_LD0 | 1 << port.DB_LD1),

    # SP Register Operations
    'SP_LDL': np.uint32(1 << port.DB_LD0 | 1 << port.DB_LD2),
    'SP_LDH': np.uint32(1 << port.DB_LD1 | 1 << port.DB_LD2),
    'SP_INC': np.uint32(1 << port.MB_INC0 | 1 << port.MB_INC1 ),
    'SP_DEC': np.uint32(1 << port.MB_DEC),
    'SP_OUT': np.uint32(1 << port.MB_OE0 | 1 << port.MB_OE1 ),

    # MAR Register Operations
    'MAR_LDH': np.uint32(1 << port.DB_LD1),
    'MAR_LDL': np.uint32(1 << port.DB_LD0),
    'MAR_OUT': np.uint32(1 << port.MB_OE0),
    'MAR_INC': np.uint32(1 << port.MB_INC0),
    'MAR_LOW': 0,

    # A Register Operations
    'A_LD': np.uint32(1 << port.DB_LD3 | 1 << port.DB_LD1 | 1 << port.DB_LD0),
    'A_OUT_LHB': np.uint32(1 << port.LBE0 | 1 << port.LBE1),
    'A_OUT_RHB': np.uint32(1 << port.RBE0 | 1 << port.RBE1),

    # T Register Operations
    'T_OUT_RHB': np.uint32(1 << port.RBE2),
    'T_OUT_LHB': np.uint32(1 << port.LBE2),
    'T_LD': np.uint32(1 << port.DB_LD3 | 1 << port.DB_LD2),

    # X Register Operations
    'X_OUT_RHB': np.uint32(1 << port.RBE0),
    'X_OUT_LHB': np.uint32(1 << port.LBE0),
    'X_LD': np.uint32(1 << port.DB_LD3 | 1 << port.DB_LD0),

    # Y Register Operations
    'Y_OUT_LHB': np.uint32(1 << port.LBE1),
    'Y_OUT_RHB': np.uint32(1 << port.RBE1),
    'Y_LD': np.uint32(1 << port.DB_LD3 | 1 << port.DB_LD1),

    # P Register Operations
    'FLD': np.uint32(1 << port.DB_LD0 | 1 << port.DB_LD1 | 1 << port.DB_LD2 | 1 << port.DB_LD3),
    'FOE': np.uint32(1 << port.ALU_OE2 | 1 << port.ALU_OE0 ),
    'C_OUT_LHB': np.uint32(1 << port.LBE2 | 1 << port.LBE0),
    'LATCHNZ': np.uint32(1 << port.LATCHNZ),
    'LATCHCV': np.uint32(1 << port.LATCHCV),
    'LATCHALL': np.uint32(1 << port.LATCHCV | 1 << port.LATCHNZ),

    # RAM
    'RAM_IN': np.uint32(1 << port.DB_LD0 | 1 << port.DB_LD2 | 1 << port.DB_LD3),
    'RAM_OUT': np.uint32(1 << port.RBE0 | 1 << port.RBE1 | 1 << port.RBE2),
    'IR_IN': np.uint32(1 << port.DB_LD1 | 1 << port.DB_LD2 | 1 << port.DB_LD3),

    # SYSTEM
    'EOC': np.uint32(1 << port.EOC),
    'XFER_LOW': np.uint32(1 << port.RBE0 | 1 << port.RBE2),
    'XFER_HIGH': np.uint32(1 << port.RBE1 | 1 << port.RBE2),
    'XFER_DB': (1 << port.RBE0 | 1 << port.RBE1 | 1 << port.RBE2),
    'ISET': (1 << port.SYS0),
    'ICLR': (1 << port.SYS1),
    'WAIT': np.uint32(1 << port.SYS0 | 1 << port.SYS1),
    'HLT': np.uint32(1 << port.SYS2),
    'CLR_RST': np.uint32(1 << port.SYS0 | 1 << port.SYS2),

    #FETCH = BASE ^ PC_OUT ^ RAM_OUT ^ RH_PASS ^ IR_IN ^ PC_INC
    'FETCH': np.uint32(0) ^ np.uint32(1 << port.MB_OE1) ^ np.uint32(1 << port.RBE0 | 1 << port.RBE1 | 1 << port.RBE2) ^  np.uint32(1 << port.ALU_OE2) ^ np.uint32(1 << port.DB_LD1 | 1 << port.DB_LD2 | 1 << port.DB_LD3) ^ np.uint32(1 << port.MB_INC1)
}

def control(name):
    #print(f"Control: {name}  VALUE: {CONTROLS.get(name)}")
    return CONTROLS.get(name)
