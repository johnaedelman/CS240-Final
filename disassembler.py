import sys

# dictionary for op codes
op_codes = {
    "000000": "add",
    "000000": "sub",
    "000000": "and",
    "000000": "or",
    "000000": "slt",
    "100011": "lw",
    "101011": "sw",
    "000100": "beq",
    "000101": "bne",
    "001000": "addi",
    "000010": "j",
    "000000": "div",
    "000000": "mfhi",
    # custom op codes (10 total)
    "000000": "kill",
    "000000": "revive",
    "000000": "heal",
    "111110": "roll",
    "000000": "boost",
    "110111": "hurt",
    "000000": "hit",
    "000000": "curse",
    "000000": "charge",
    "111000": "absorb"
}
# dictionary for function codes (R-type only)
func_codes = {
    "100000": "add",
    "100010": "sub",
    "100100": "and",
    "100101": "or",
    "101010": "slt",
    "011010": "div",
    "010000": "mfhi",
    "001100": "syscall",
    # custom function codes 
    "101110": "kill",
    "111010": "revive",
    "111100": "heal",
    "100110": "boost",
    "011100": "hit",
    "010110": "curse",
    "111001": "charge"
}

# dictionary for registers
registers = {
    "00000": "$zero",
    "00001": "$at",
    "00010": "$v0",
    "00011": "$v1",
    "00100": "$a0",
    "11100": "$gp",
    "01000": "$t0",
    "01001": "$t1",
    "01010": "$t2",
    "01011": "$t3",
    "01100": "$t4",
    "01101": "$t5",
    "01110": "$t6",
    "01111": "$t7",
    "10000": "$s0",
    "10001": "$s1",
    "10010": "$s2",
    "10011": "$s3",
    "10100": "$s4",
    "10101": "$s5",
    "10110": "$s6",
    "10111": "$s7",
}

labels = {}

# open and read binary file
def handle_lines(bin_file: str, mips_file: str):
    input_file = open(bin_file, "r")
    # sort lines into list/ removes whitespace
    line = input_file.readlines()[0].strip()
    mips_instructions = bin_to_mips(line) # convert
    # write to output file
    output_file = open(mips_file, "w")
    for instruction in mips_instructions:
        output_file.write(instruction)
        output_file.write("\n")


def convert_offset(offset: str, num_bits: int):
    if offset.startswith("0"):
        return int(offset, 2)
    elif offset.startswith("1"):  # convert from two's complement signed
        return int(offset, 2) - (1 << num_bits)
# function for conversion
def bin_to_mips(line):
    mips = []
    line_count = 0
    offsets = {}
    bit_string = ""
    # add every bit in line to bit_string
    for i in range(0, len(line)):
        bit_string += line[i]
        # if line has 32 bits, isolate opcode
        if len(bit_string) == 32:
            line_count += 1
            op_code = bit_string[0:6]
            # if R-type, assign others accordingly
            if op_code == "000000":

                # division
                func_code = bit_string[26:32]

                if func_code == "011010":
                    rs = bit_string[6:11]
                    rt = bit_string[11:16]
                    rd = "000000"
                    shift = "000000"
                    mips.append(
                        f"{func_codes[func_code]} {registers[rs]}, {registers[rt]}"
                    )
                    print(f"TEST: div instructions: {op_code} {rs} {rt} {rd} {shift} {func_code} --> {func_codes[func_code]} {registers[rs]} {registers[rt]}")
                
                # custom instructions with 2 registers --> kill, revive, heal, boost, curse, hit
                elif func_code in ["101110", "111010", "111100", "100110", "010110", "011100"]:
                    rs = bit_string[6:11]
                    rt = bit_string[11:16]
                    rd = "000000"
                    shift = "000000"
                    mips.append(
                        f"{func_codes[func_code]} {registers[rs]}, {registers[rt]}"
                    )
                    print(f"TEST: 2 register custom instructions: {op_code} {rs} {rt} {rd} {shift} {func_code} --> {func_codes[func_code]} {registers[rs]} {registers[rt]}")
               
                # single register instructions (mfhi, charge)
                elif func_code in ["010000", "111001"]:
                    rd = bit_string[16:21]
                    mips.append(
                        f"{func_codes[func_code]} {registers[rd]}"
                    )
                    print(f"TEST: single register instructions: {op_code} 00000 00000 {rd} 00000 {func_code} --> {func_codes[func_code]} {registers[rd]}")

                # other R-type instructions
                else:
                    rs, rt, rd, shift, func_code = (
                        # slices string into sections
                        bit_string[6:11],
                        bit_string[11:16],
                        bit_string[16:21],
                        bit_string[21:26],
                        bit_string[26:32], # slices correctly
                    )
                    # add function instructions and registers in correct order with commas from dictionary
                    mips.append(
                        f"{func_codes[func_code]} {registers[rd]}, {registers[rs]}, {registers[rt]}"
                    )
                    print(f"TEST: other R-type instructions: {op_code} {rs} {rt} {rd} {shift} {func_code} --> {func_codes[func_code]} {registers[rd]} {registers[rs]} {registers[rt]} ")

            # for roll/absorb instruction (one register, one immediate)
            elif op_code == "111110":
                rs = bit_string[6:11]
                offset = bit_string[16:32]
                mips.append(
                        f"{op_codes[op_code]} {registers[rs]}, {int(offset, 2)}"
                    )
                print(f"TEST: one register and immediate custom instruction: {op_code} {rs} 00000 {offset} --> {op_codes[op_code]} {registers[rs]}, {int(offset, 2)}")
            # otherwise if lw or sw op-codes (I-type)
            elif op_code in ["100011", "101011"]:
                # assign registers accordingly
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                # instruction name and registers with offset()
                mips.append(
                    f"{op_codes[op_code]} {registers[rt]}, {int(offset, 2)}({registers[rs]})"
                )
                print(f"TEST: lw or sw instructions: {op_code} {rs} {offset} {rt} --> {op_codes[op_code]} {registers[rt]}, {int(offset, 2)}({registers[rs]})")
            # j-type instructions: | opcode (6 bits) | target (26 bits) |
            elif op_code == "000010":
                offset = bit_string[6:]
                mips.append(
                    f"{op_code} {convert_offset(offset, 26)}"
                )
                offsets[line_count] = convert_offset(offset, 26)
                print(f"TEST: jump instructions: {op_code} {offset} --> {op_codes[op_code]} (target address)")

            # check for beq and blt
            elif op_code in ["000100", "000101"]:
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {convert_offset(offset, 16)}"
                )
                offsets[line_count] = convert_offset(offset, 16)
                print(f"TEST: beq instructions: {op_code} {rs} {rt} {offset} --> {op_codes[op_code]} {registers[rs]} {registers[rt]} (target address)")

            else: # I-type instructions for others like addi
                rt, rs, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {int(offset, 2)}"
                )
                print(f"TEST: Other I-type instructions: {op_code} {rt} {rs} {offset} --> {op_codes[op_code]} {registers[rs]} {registers[rt]} {int(offset, 2)}")
            
            bit_string = ""
    print(offsets)
    label_count = 0
    for o in offsets:
        index = o + offsets[o] + label_count - 1
        if not mips[index].strip("\n").endswith(":"):  # If there's no label there already
            mips.insert(index, f"label{label_count}:")
            label_count += 1
    return mips

# if __name__ == "__main__":
    # handle_lines(sys.argv[1])


handle_lines("custom_machine_code.txt", "BACK_TO_MIPS.txt")
