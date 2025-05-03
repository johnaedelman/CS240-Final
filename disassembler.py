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
    # custom op codes
    "000000": "kill",
    "000000": "revive",
    "000000": "heal",
    "111110": "roll",
    "000000": "boost",
    "000000": "hurt",
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
    # custom function codes 
    "101110": "kill",
    "111010": "revive",
    "111100": "heal",
    "100110": "boost",
    "000100": "hurt",
    "010000": "hit",
    "010110": "curse",
    "111001": "charge"
    # skipped roll and absorb (I-types)
}

# dictionary for registers
registers = {
    "00000": "$zero",
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
def handle_lines(bin_file: str):
    input_file = open(bin_file, "r")
    # sort lines into list/ removes whitespace
    line = input_file.readlines()[0].strip()
    mips_instructions = bin_to_mips(line) # convert
    # write to output file
    output_file = open("BACK_TO_MIPS.txt", "w")
    for instruction in mips_instructions:
        output_file.write(instruction)
        output_file.write("\n")

# function for conversion
def bin_to_mips(line):
    mips = []
    bit_string = ""
    # add every bit in line to bit_string
    for i in range(0, len(line)):
        bit_string += line[i]
        # if line has 32 bits, isolate opcode
        if len(bit_string) == 32:
            op_code = bit_string[0:6]
            print(op_code)
            # if R-type, assign others accordingly
            if op_code == "000000":
                rs, rt, rd, shift, func_code = (
                    # slices string into sections
                    bit_string[6:11],
                    bit_string[11:16],
                    bit_string[16:21],
                    bit_string[21:26],
                    bit_string[26:32],
                )
                # add function instructions and registers in correct order with commas from dictionary
                mips.append(
                    f"{func_codes[func_code]} {registers[rd]}, {registers[rs]}, {registers[rt]}"
                )
            # otherwise if lw or sw op-codes (I-type)
            elif op_code in ["100011", "101011"]:
                # assign registers accordingly
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                # instruction name and registers with offset()
                mips.append(
                    f"{op_codes[op_code]} {registers[rt]}, {int(offset, 2)}({registers[rs]})"
                )
            
            else: # I-type instructions that are not lw or sw
                rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
                mips.append(
                    f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {int(offset, 2)}"
                )

            bit_string = ""
    return mips

if __name__ == "__main__":
    handle_lines(sys.argv[1])

