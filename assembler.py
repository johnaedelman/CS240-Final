import sys
import os

# hash tables!
# keys on left and values on right
op_codes = {
    "add": "000000",
    "sub": "000000",
    "and:": "000000",
    "or:": "000000",
    "slt": "000000",
    "lw": "100011",
    "sw": "101011",
    "beq": "000100",
    "bne": "000100",
}
# function codes (end)
func_codes = {
    "add": "100000",
    "sub": "100010",
    "and": "100100",
    "or": "100101",
    "slt": "101010",
}
# all registers
registers = {
    "$zero": "00000",
    "$t1": "01001",
    "$t2": "01010",
    "$t3": "01011",
    "$t4": "01100",
    "$t5": "01101",
    "$t6": "01110",
    "$t7": "01111",
    "$s0": "10000",
    "$s1": "10001",
    "$s2": "10010",
    "$s3": "10011",
    "$s4": "10100",
    "$s5": "10101",
    "$s6": "10110",
    "$s7": "10111",
}
# for shamt field, r-type
shift_logic_amount = "00000"

# param is a file name/path as a string
def interpret_line(mips_file: str):
    # open input file (readable)
    input_file = open(mips_file, "r")
    # open output file (writable)
    output_file = open("mips_to_bin.txt", "w")
    # reads input file line by line
    for instruction in input_file:
        # call assemble() and write to output file
        bin = assemble(instruction)
        output_file.write(bin)

# function to assemble
def assemble(line):
    # splits line at #, and removes whitespaces before/after
    line = line.split("#")[0].strip()

    # if line is empty after ^, do nothing
    if not line:
        return

    # split line using spaces as delimiter
    parts = line.split(" ")
    # first part is op code
    op_code = parts[0]

    # checks if op_code is in function codes dictionary
    if op_code in func_codes:
        # assigns tuple to 3 variables
        rd, rs, rt = (
            # get rid of commas in registers 2, 3, and 4
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
            parts[3].replace(",", ""),
        )

        return (
            # accesses value at op-code dictionary
            op_codes[op_code]
            # adds source register value from rs dictionary
            + registers[rs]
            # adds second source register value from rt dictionary
            + registers[rt]
            # adds third register from rd dictionary
            + registers[rd]
            # adds shamt section
            + shift_logic_amount
            # adds function codes from op-code dictionary
            + func_codes[op_code]
        )
    
    if op_code in ["lw", "sw", "beq"]:
        if op_code == "lw" or op_code == "sw":
            rt = parts[1].replace(",", "")
            # splits into [0, $s2] assigns to each variable
            offset, rs = parts[2].replace(")", "").split("(")
            # turns offset into int, replaces with 0b, pads front with 0's until 16
            offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            # retrieves values based on keys, dict[key]
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin
        else:
            rs, rt, offset = (
                # removes commas
                parts[1].replace(",", ""),
                parts[2].replace(",", ""),
                parts[3].replace(",", ""),
            )

            offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            # make dictionary, key = string label, value = offset
            
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin

# python script running directly?
if __name__ == "__main__":
    # open and interpret mips file
    mips_file = "program1.mips"
    interpret_line(mips_file)