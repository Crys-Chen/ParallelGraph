import sys
import re
import argparse
from data import *
from inst import *
from param import *
from graph import *

parser = argparse.ArgumentParser(description='')
# 给这个解析对象添加命令行参数
parser.add_argument('--filename', type=str)
args = parser.parse_args()

def read_file(filename):
    with open(filename, 'r') as file:
        log_content = file.read()
        log_entries = log_content.strip().split('\n')
        insts = []

        for entry in log_entries:
            step_match = re.search(r'current_step\s*=\s*(\d+)', entry)
            self_match_initial = re.search(r'self:\s*(\w+)\((\w+)\(([^)]+)\)\)', entry)
            self_match_inter = re.search(r'self:\s*(\w+)\((\w+)\(([^)]+)\), (\w+)\(([^)]+)\)\)', entry)

            assert step_match and (self_match_initial or self_match_inter)
            current_step = int(step_match.group(1))
            if self_match_inter is None:
                operation = self_match_initial.group(1)
                if operation == "Store":
                    type = INST.Store
                elif operation == "Add":
                    type = INST.Add
                elif operation == "Sub":
                    type = INST.Sub
                elif operation == "Mul":
                    type = INST.Mul
                else:
                    assert 0

                index = self_match_initial.group(3)
                if "," in index:
                    matrix = Matrix(self_match_initial.group(2))
                    row_and_col = index.split(", ")
                    element = MatrixElement(matrix, int(row_and_col[0]), int(row_and_col[1]))
                    insts.append(MetaInstruction(current_step, type, [element]))
                else:
                    vector = VectorElement(self_match_initial.group(2), int(index))
                    insts.append(MetaInstruction(current_step, type, [vector]))
                
            else:
                
                operation = self_match_inter.group(1)
                previous = set()
                depend = set()
                inputs = []

                src = self_match_inter.group(2)
                if src == "Intermediate":
                    index = int(self_match_inter.group(3))
                    inputs.append(insts[index].output)
                    depend.add(index)
                    previous.add(index)
                    depend = depend.union(insts[index].depend)
                elif src == "Constant":
                    inputs.append(VectorElement(src, int(self_match_inter.group(3))))
                else:
                    print("error: ", src)
                    assert 0

                src = self_match_inter.group(4)
                if src == "Intermediate":
                    index = int(self_match_inter.group(5))
                    inputs.append(insts[index].output)
                    previous.add(index)
                    depend.add(index)
                    depend = depend.union(insts[index].depend)
                elif src == "Constant":
                    inputs.append(VectorElement(src, int(self_match_inter.group(5))))
                else:
                    print("error: ", src)
                    assert 0

                if operation == "Store":
                    type = INST.Store
                elif operation == "Add":
                    type = INST.Add
                elif operation == "Sub":
                    type = INST.Sub
                elif operation == "Mul":
                    type = INST.Mul
                else:
                    assert 0

                insts.append(MetaInstruction(current_step, type, inputs, previous, depend))

        return insts
    
def SIMD(filename):
    meta_insts = read_file(filename)
    combined_insts = []
    print("Original: \n", meta_insts)
    for meta_inst in meta_insts:
        for combined_inst in combined_insts:
            if combined_inst.try_absorb(combined_insts, meta_inst):
                break
        else:
            combined_insts.append(CombinedInstruction(len(combined_insts), meta_inst, combined_insts))
    print("Combined: \n", combined_insts)
    print("Number of SIMDs: ", len(combined_insts))
    # for inst in combined_insts:
    #     if len(inst.previous) > 2:
    #         print("here: \n", inst)
    build_graph(combined_insts)



if __name__=="__main__":
    SIMD(args.filename)