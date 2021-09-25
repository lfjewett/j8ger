import numpy as np
from controls import control

class opcode():
    def __init__(self, code, **kwargs):
        self.code = code
        self.syntax = kwargs.get('syntax')
        self.description = kwargs.get('description')
        self.flags = kwargs.get('flags')
        self.length = kwargs.get('length')
        self.cycles = kwargs.get('cycles')
        self.mode = kwargs.get('mode')
        for step in kwargs.get('steps'):
            for key in step:
                x = np.uint32(0)
                for word in step[key]:
                    x = x ^ control(word)
                step[key] = x
        self.steps = kwargs.get('steps')
