from data import *
from enum import Enum

INST = Enum("INST", ("Store", "Add", "Mul", "Sub"))

class Instruction:
    def __init__(self, 
                 type: INST,
                 src: Source,
                 previous: set,
                 depend: set) -> None:
        self.type = type
        self.src = src
        self.previous = previous
        self.depend = depend

    def combinable(self, other):
        return self.type == other.type and self.src == other.src
    
    def __repr__(self) -> str:
        type = "\n\tType: " + str(self.type)[5:]
        previous = "\n\tPrevious: " + str(self.previous)
        depend = "\n\tDepend: " + str(self.depend)
        return "\nInst: " + type + previous + depend + self.src.__repr__()

class MetaInstruction(Instruction):
    def __init__(self,
                 step: int,
                 type: INST,
                 inputs: "list[Data]",
                 previous: set = set(),
                 depend: set = set()) -> None:
        self.step = step
        self.type = type
        self.inputs = inputs
        src = Source()
        for input in inputs:
            src.combine(input.src)

        super().__init__(type, src, previous, depend)

        self.output = InterData(self.src, self.step)
        
    def __repr__(self) -> str:
        inputs_str = "\n\tInputs: "
        for input in self.inputs:
            inputs_str += input.__repr__()
        return super().__repr__().replace("Inst: ", "Inst: "+str(self.step)) + inputs_str 


class CombinedInstruction(Instruction):
    def __init__(self, 
                 step: int,
                 inst: MetaInstruction,
                 combined_insts: "list[CombinedInstruction]",
                 ) -> None:
        self.step = step
        self.type = inst.type
        super().__init__(inst.type, inst.src, set(), set())
        self.insts = {inst.step}
        self.output = InterData(inst.src, self.step)
        # self.depend = set()
        for combined_inst in combined_insts:
            if len(inst.depend.intersection(combined_inst.insts)) != 0:
                self.depend.add(combined_inst.step)
            if len(inst.previous.intersection(combined_inst.insts)) != 0:
                self.previous.add(combined_inst.step)

    def try_absorb(self, 
                   combined_insts: "list[CombinedInstruction]",
                   inst: MetaInstruction):
        if self.type != inst.type or self.src != inst.src:
            return False
        combined_previous = set()
        combined_depend = set()
        for combined_inst in combined_insts:
            if len(inst.depend.intersection(combined_inst.insts)) != 0:
                combined_depend.add(combined_inst.step)
            if len(inst.previous.intersection(combined_inst.insts)) != 0:
                combined_previous.add(combined_inst.step)
        if not combined_depend.issubset(self.depend):
            return False
        if len(inst.depend.intersection(self.insts)) != 0 or \
            inst.step in self.depend or (len(self.depend) != 0 and self.depend.issubset(inst.depend)):
            # if not (len(inst.depend.intersection(self.insts)) != 0 or inst.step in self.depend):
            print("here: ", self.insts, inst.step, self.depend, inst.depend, self.src, inst.src)
            return False
        
        self.insts.add(inst.step)
        self.previous = self.previous.union(combined_previous)
        # self.depend = self.depend.union(inst.depend)
        # self.depend.union(combined_depend)
        # print("look: ", self.depend)
                
        return True

    def __repr__(self) -> str:
        inputs_str = "\n\tOriginal instructions: "
        for inst in self.insts:
            inputs_str += str(inst) + " "
        return super().__repr__().replace("Inst: ", "Inst: "+str(self.step)) + inputs_str
