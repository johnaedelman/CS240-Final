import sys
import os

# keys on left and values on right
op_codes = {
    "add": "000000",
    "sub": "000000",
    "div": "000000",
    "mfhi": "000000",
    "and": "000000",
    "or": "000000",
    "slt": "000000",
    "syscall": "000000",
    "addi": "001000",
    "j": "000010",
    "lw": "100011",
    "sw": "101011",
    "beq": "000100",
    "bne": "000100",
    # custom op codes
    "kill": "000000",
    "revive": "000000",
    "heal": "000000",
    "roll": "111110",
    "boost": "000000",
    "hurt": "110111",
    "hit": "000000",
    "curse": "000000",
    "charge": "000000",
    "absorb": "111000"
}

# function codes (end)
# Standard = instructions w/form [6-bit opcode] [5-bit register]x3 [5-bit shamt] [6-bit func code]
standard_func_codes = {
    "add": "100000",
    "sub": "100010",
    "and": "100100",
    "or": "100101",
    "slt": "101010",
    "charge": "111001"
}

# Instructions that have func codes at the end, but do not match the form of add or sub
special_func_codes = {
    "div": "011010",
    "mfhi": "010000",
    "syscall": "001100",
    # custom function codes
    "kill": "101110",
    "revive": "111010",
    "heal": "111100",
    "boost": "100110",
    "hit": "011100",
    "curse": "010110",
}

# all registers
registers = {
    "$zero": "00000",
    "$at": "00001",
    "$v0": "00010",
    "$v1": "00011",
    "$a0": "00100",
    "$a1": "00101",
    "$a2": "00110",
    "$a3": "00111",
    "$t0": "01000",
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
    "$gp": "11100"
}
# for shamt field, r-type
shift_logic_amount = "00000"
current_line = 1
labels = {}
strings = {}
reading_strings = False
gp_offset = 0


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
        output_file.write(str(bin))  # cast to string

# function to assemble
def assemble(line):
    global current_line, reading_strings, gp_offset
    # splits line at #, and removes whitespaces before/after
    line = line.split("#")[0].strip()

    # if line is empty after ^, do nothing
    if not line:
        return ""

    # split line using spaces as delimiter
    parts = line.split(" ")
    # first part is op code
    op_code = parts[0]

    # Store defined strings in memory
    if op_code == ".data":
        reading_strings = True
        return ""
    elif op_code == ".text":
        reading_strings = False
        return ""
    if reading_strings:
        strings[op_code.strip(":")] = str(gp_offset)
        string_instructions = ""
        for char in parts[2].strip("\""):
            string_instructions += f"001000{registers["$zero"]}{registers["$at"]}{bin(ord(char)).replace("0b", "").zfill(16)}\n"
            # Store the ASCII numerical representation of the char inside of $at
            string_instructions += f"101011{registers["$gp"]}{registers["$at"]}{bin(int(gp_offset)).replace("0b", "").zfill(16)}\n"
            # Store each individual char in a sequential area of memory
            gp_offset += 1
            current_line += 2
            # Store each char in the global data area using sw
        string_instructions += f"001000{registers["$zero"]}{registers["$at"]}{"".zfill(16)}\n"
        string_instructions += f"101011{registers["$gp"]}{registers["$at"]}{bin(int(gp_offset)).replace("0b", "").zfill(16)}\n"
        # Null-terminate string
        gp_offset += 1
        current_line += 2
        return string_instructions

    # Keep track of labels
    if op_code[len(op_code) - 1] == ":":
        op_code = op_code.strip(":")
        if op_code in labels:
            labels[op_code].append(
                float(current_line - 1))  # Convert to float to mark it as the initial definition of the label
        else:
            labels[op_code] = [float(current_line - 1)]
        return ""

    pre_instruction = ""  # For pseudo-instructions that require other operations in order to work

    # Converting pseudo-instructions into simple instructions
    if op_code == "li":
        op_code = "addi"
        parts.append(parts[2])
        parts[2] = "$zero"
        # set original register to zero + immediate
    elif op_code in ["move", "la"]:
        if op_code == "move":
            op_code = "add"
            parts.append("$zero")
            # add source and zero into dest
        elif op_code == "la":  # Loads the offset from $gp at which the string begins into rd
            op_code = "addi"
            parts[2] = strings[parts[2]]  # Immediate value of the memory offset from $gp
            parts.append(parts[2])
            parts[2] = "$zero"
            # addi rd, $zero, memory offset

    elif op_code == "ble":
        rs, check = (
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),  # can be immediate or register
        )
        if not check.startswith("$"):
            pre_instruction += f"001000{registers["$zero"]}{registers["$at"]}{to_signed_bin(int(check), 16)}\n"
        else:
            pre_instruction += f"000000{registers["$zero"]}{registers[check]}{registers["$at"]}00000100000\n"
        # load immediate value into $at
        pre_instruction += f"000000{registers["$at"]}{registers[rs]}{registers["$at"]}00000101010\n"
        # slt $at, $at, rs ($at will be zero if rs is less than the provided immediate)
        current_line += 2
        op_code = "beq"
        parts[1] = "$at"
        parts[2] = "$zero"
        # Now it becomes a standard beq, except the checked condition is whether or not the provided register is less than the immediate
    # checks if op_code is in function codes dictionary
    if op_code in standard_func_codes:
        # assigns tuple to 3 variables
        rd, rs, rt = (
            # get rid of commas in registers 2, 3, and 4
            parts[1].replace(",", ""),
            parts[2].replace(",", ""),
            parts[3].replace(",", ""),
        )
        current_line += 1
        return (
            pre_instruction
            # accesses value at op-code dictionary
            + op_codes[op_code]
            # adds source register value from rs dictionary
            + registers[rs]
            # adds second source register value from rt dictionary
            + registers[rt]
            # adds third register from rd dictionary
            + registers[rd]
            # adds shamt section
            + shift_logic_amount
            # adds function codes from op-code dictionary
            + standard_func_codes[op_code] + "\n"
        )
    
    elif op_code in ["lw", "sw", "beq", "bne", "addi", "j", "hurt", "absorb", "roll"]:
        if op_code == "lw" or op_code == "sw":
            rt = parts[1].replace(",", "")
            # splits into [0, $s2] assigns to each variable
            offset, rs = parts[2].replace(")", "").split("(")
            # turns offset into int, replaces with 0b, pads front with 0's until 16
            offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
            # retrieves values based on keys, dict[key]
            current_line += 1
            return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin + "\n"
        elif op_code == "beq" or op_code == "bne":
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
            current_line += 1
            return pre_instruction + op_codes[op_code] + registers[rs] + registers[rt] + offset + "\n"
        elif op_code == "addi":
            rs, rt, immediate = (
                # removes commas
                parts[1].replace(",", ""),
                parts[2].replace(",", ""),
                parts[3].replace(",", "")
            )
            immediate = to_signed_bin(int(immediate), 16)
            current_line += 1
            return pre_instruction + op_codes[op_code] + registers[rt] + registers[rs] + immediate + "\n"
        
        # roll custom instruction roll $t1, 16
        elif op_code == "roll":
            # removes commas
            rs, immediate = (
                # removes commas
                parts[1].replace(",", ""),
                parts[2].replace(",", ""),
            )
            current_line += 1
            print(f"TESTING ROLL: {op_code} {rs} {immediate} --> {op_codes[op_code]} {registers[rs]} 00000 {to_signed_bin(int(immediate), 16)}\n")
            return op_codes[op_code] + registers[rs] + "00000" + to_signed_bin(int(immediate), 16) + "\n"
            

        # for hurt and absorb
        elif op_code in ["hurt", "absorb"]:
            rs, rt, immediate = (
                # removes commas
                parts[1].replace(",", ""),
                parts[2].replace(",", ""),
                parts[3].replace(",", ""),
            )
            immediate = to_signed_bin(int(immediate), 16)
            current_line += 1
            print(f"I-type custom instructions: {op_code} {rt} {rs} --> {op_codes[op_code]} {registers[rt]} {registers[rs]} {immediate}\n")
            return op_codes[op_code] + registers[rt] + registers[rs] + immediate + "\n"
        elif op_code == "j":
            offset = parts[1]
            if offset in labels:
                labels[offset].append(current_line)
            else:
                labels[offset] = [current_line]
            current_line += 1
            return op_codes[op_code] + offset + "\n"

    elif op_code in special_func_codes:
        # div and custom 2 register instructions
        if op_code in ["div", "kill", "revive", "heal", "boost", "curse", "hit"]:
            rs, rt = (
                parts[1].replace(",", ""),
                parts[2].replace(",", "")
            )
            current_line += 1
            print(f"2 register instructions: {op_code} {rs} {rt} --> {op_codes[op_code]} {registers[rs]} {registers[rt]} 00000 00000 {special_func_codes[op_code]}\n")
            return op_codes[op_code] + registers[rs] + registers[rt] + "0000000000" + special_func_codes[op_code] + "\n"
        # mfhi and charge
        elif op_code in ["mfhi"]:
            rd = parts[1].replace(",", "")
            current_line += 1
            print(f"1 register instructions: {op_code} {rd} --> {op_codes[op_code]} 00000 00000 {registers[rd]} 00000 {special_func_codes[op_code]}")
            return op_codes[op_code] + "0000000000" + registers[rd] + "00000" + special_func_codes[op_code] + "\n"
        elif op_code == "syscall":
            current_line += 1
            return op_codes[op_code] + "00000000000000000000" + special_func_codes[op_code] + "\n"


def to_signed_bin(num, num_bits):  # Converts an int to a signed two's complement binary number
    if num < 0:
        num = (1 << num_bits) + num
    return bin(num)[2:].zfill(num_bits)  # Works for values within the range [(2^num_bits/2) - 1, (-2^num_bits)/2]


def handle_labels(bin_filename: str):
    bin_file = open(bin_filename, "r")
    lines = bin_file.read()
    print(lines)
    bin_file.close()
    lines = lines.split("\n")
    if "" in lines:
        lines.remove("") # if an empty string exists remove it

    for label in labels:
        definition_line = 0
        for i in range(len(labels[label])):
            if isinstance(labels[label][i], float):
                definition_line = int(labels[label][i])
                labels[label].pop(i)
                break
        for val in labels[label]:
            offset = definition_line - val  # How many lines to jump away from the current line
            if lines[val - 1][0:6] == op_codes["j"]:
                n_bits = 26
            else:
                n_bits = 16
            lines[val - 1] = lines[val - 1].replace(label, to_signed_bin(offset, n_bits))  # Replace the placeholder label name with the correct offset
    bin_file = open(bin_filename, "w")
    bin_file.writelines(lines)
    bin_file.close()


# python script running directly?
if __name__ == "__main__":
    # open and interpret mips file
    mips_file = "boss_fight.txt"    # "program1.mips"
    binary_file = "assembler_output.txt"      # "mips_to_bin.txt"
    interpret_line(mips_file, binary_file)
    handle_labels(binary_file)
