import sched
import time
from enum import Enum

class Symbol(Enum):
    ONE = 1,
    ZERO = 0,
    BLANK = 2

class State(Enum):
    START = 0
    HALT = 1

class Move(Enum):
    RIGHT = 1,
    LEFT = 2,
    STAY = 3

class Instruction:

    def __init__(self, cur_state, read_symbol, write_symbol, direction, next_state):
        self.cur_state = cur_state
        self.read_symbol = read_symbol
        self.write_symbol = write_symbol
        self.direction = direction
        self.next_state = next_state

class TuringMachine:

    def __init__(self, clock_speed=1):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.clock_speed = clock_speed
        self.tapesize = 16*1024*1024
        self.needle = self.tapesize // 2
        self.tape = self.tapesize * [0]
        self.state = State.START
        self.executable = {}

    def execute(self, program):
        self.parse(program)
        self.run()
    
    def run(self):

        if self.state == State.HALT:
            print("[Halt] {0}".format(self.read()))
            return

        key = (self.state, self.read())
        if not key in self.executable:
            raise OSError("Runtime Error: Instruction not found : {0}".format(key))
        value = self.executable[key]

        print("[Executing] {0} -> {1}".format(key, value))

        self.state = value[0]
        self.write(value[1])
        self.move(value[2])

        self.scheduler.enter(self.clock_speed, 1, self.run)
        self.scheduler.run()

    def parse(self, program):
        self.executable = {}
        for p in program:
            key = (p.cur_state, p.read_symbol)
            value = (p.next_state, p.write_symbol, p.direction)

            if key in self.executable:
                raise OSError("Ambiguous code")
            self.executable[key] = value
        start_keys = [
            (State.START, Symbol.ONE),
            (State.START, Symbol.ZERO),
            (State.START, Symbol.BLANK),
        ]

        error = True
        for sk in start_keys:
            if sk in self.executable:
                error = False
        if error:
            raise OSError("No start state")
    
    def move(self, direction):
        if direction == Move.RIGHT:
            self.needle += 1
        elif direction == Move.LEFT:
            self.needle -= 1
        else:
            self.needle = self.needle
    
    def read(self):
        if self.tape[self.needle] == 0:
            return Symbol.ZERO
        elif self.tape[self.needle] == 1:
            return Symbol.ONE
        else:
            return Symbol.BLANK
    
    def write(self, symbol):
        if symbol == Symbol.ZERO:
            self.tape[self.needle] = 0
        elif symbol == Symbol.ONE:
            self.tape[self.needle] = 1
        else:
            self.tape[self.needle] = 2


class Compiler:

    def __init__(self):
        self.state = {
            "start": State.START,
            "stop": State.HALT
        }

        self.symbol = {
            "1": Symbol.ONE,
            "0": Symbol.ZERO,
            "null": Symbol.BLANK
        }

        self.move = {
            "l": Move.LEFT,
            "r": Move.RIGHT,
            "s": Move.STAY
        }

    def compile(self, filepath):
        program = []
        lines = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            l = line.strip()
            if len(l) == 0:
                continue
            elif l[0] == '#':
                # comment
                continue
            tokens = l.split(" ")
            if len(tokens) != 5:
                raise OSError("Syntax Error : [{0}] {1}".format(i+1, line))

            cur_state = tokens[0].strip()
            read_symbol = tokens[1].strip()
            write_inst = tokens[2].strip()
            move_direction = tokens[3].strip()
            next_state = tokens[4].strip()

            nullerror = len(cur_state)*len(read_symbol)*len(write_inst)*len(move_direction)*len(next_state)
            if nullerror == 0:
                raise OSError("Syntax Error : [{0}] {1}".format(i+1, line))

            cur_state = self.state[cur_state] if cur_state in self.state else cur_state
            next_state = self.state[next_state] if next_state in self.state else next_state

            try:
                inst = Instruction(
                    cur_state,
                    self.symbol[read_symbol],
                    self.symbol[write_inst],
                    self.move[move_direction],
                    next_state
                )
                program.append(inst)
            except:
                raise OSError("Syntax Error : [{0}] {1}".format(i+1, line))
        return program

if __name__ == "__main__":
    

    """
    program = []
    program.append(Instruction(State.START, Symbol.ZERO, Symbol.ONE, Move.RIGHT, "1"))
    program.append(Instruction("1", Symbol.ZERO, Symbol.BLANK, Move.LEFT, State.START))
    program.append(Instruction(State.START, Symbol.ONE, Symbol.BLANK, Move.STAY, State.HALT))

    m = TuringMachine()
    m.execute(program)
    """
    c = Compiler()
    program = c.compile("sample-code.txt")
    m = TuringMachine()
    m.execute(program)
    #program.append(Instruction(State.START, Symbol.ZERO, Symbol.ONE, Move.RIGHT, State.START))