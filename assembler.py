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
current_line = 1
labels = {}


# param is a file name/path as a string
def interpret_line(mips_f: str, bin_f: str):
    # open input file (readable)
    input_file = open(mips_f, "r")
    # open output file (writable)
    output_file = open(bin_f, "w")
    # reads input file line by line
    for instruction in input_file:
        # call assemble() and write to output file
        bin = assemble(instruction)
        output_file.write(bin)

# function to assemble
def assemble(line):
    global current_line
    # splits line at #, and removes whitespaces before/after
    line = line.split("#")[0].strip()

    # if line is empty after ^, do nothing
    if not line:
        return ""

    # split line using spaces as delimiter
    parts = line.split(" ")
    # first part is op code
    op_code = parts[0]
    if op_code[len(op_code) - 1] == ":":  # If op code is a label
        op_code = op_code.strip(":")
        if op_code in labels:
            labels[op_code].append(float(current_line - 1))  # Convert to float to mark it as the initial definition of the label
        else:
            labels[op_code] = [float(current_line - 1)]
        return ""

    # checks if op_code is in function codes dictionary
    if op_code in func_codes:
        # assigns tuple to 3 variables
        rd, rs, rt = (
            # get rid of commas in registers 2, 3, and 4
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
            parts[3].replace(",", ""),
        )
        current_line += 1
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
            + func_codes[op_code] + "\n"
        )
    
    if op_code in ["lw", "sw", "beq"]:
        if op_code == "lw" or op_code == "sw":
            rt = parts[1].replace(",", "")
            # splits into [0, $s2] assigns to each variable
            offset, rs = parts[2].replace(")", "").split("(")
            # turns offset into int, replaces with 0b, pads front with 0's until 16
            offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            # retrieves values based on keys, dict[key]
            current_line += 1
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin + "\n"
        else:
            rs, rt, offset = (
                # removes commas
                parts[1].replace(",", ""),
                parts[2].replace(",", ""),
                parts[3].replace(",", ""),
            )
            if offset in labels:
                labels[offset].append(current_line)
            else:
                labels[offset] = [current_line]
            offset_bin = offset  # Temporary, to be subbed back in for binary once later calcs are made
            # offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            # make dictionary, key = string label, value = offset
            current_line += 1
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin + "\n"


def to_signed_bin(num, num_bits):  # Converts an int to a signed two's complement binary number
    if num < 0:
        num = (1 << num_bits) + num
    return bin(num)[2:].zfill(num_bits)  # Works for values within the range [(2^num_bits/2) - 1, (-2^num_bits)/2]


def handle_labels(bin_filename: str):
    bin_file = open(bin_filename, "r")
    lines = bin_file.read()
    bin_file.close()
    lines = lines.split("\n")
    lines.remove("")

    for label in labels:
        definition_line = 0
        for i in range(len(labels[label])):
            if isinstance(labels[label][i], float):
                definition_line = int(labels[label][i])
                labels[label].pop(i)
                break
        for val in labels[label]:
            offset = definition_line - val  # How many lines to jump away from the current line
            lines[val - 1] = lines[val - 1].replace(label, to_signed_bin(offset, 16))  # Replace the placeholder label name with the correct offset
    bin_file = open(bin_filename, "w")
    bin_file.writelines(lines)
    bin_file.close()


# python script running directly?
if __name__ == "__main__":
    # open and interpret mips file
    mips_file = "program1.mips"
    binary_file = "mips_to_bin.txt"
    interpret_line(mips_file, binary_file)
    handle_labels(binary_file)