registers = {
    "$zero": 0,
    "$at": 0,
    "$v0": 0,
    "$v1": 0,
    "$a0": 0,
    "$a1": 0,
    "$a2": 0,
    "$a3": 0,
    "$t0": 0,
    "$t1": 0,
    "$t2": 0,
    "$t3": 0,
    "$t4": 0,
    "$t5": 0,
    "$t6": 0,
    "$t7": 0,
    "$s0": 0,
    "$s1": 0,
    "$s2": 0,
    "$s3": 0,
    "$s4": 0,
    "$s5": 0,
    "$s6": 0,
    "$s7": 0,
    "$gp": 0x10008000,
    "hi": 0,
    "lo": 0
}

memory_locations = {}

labels = {}

def handle_lines(lines: list[str]):
    for index, line in enumerate(lines):  # Get label locations before doing anything else
        if line.strip().endswith(":"):
            labels[line.strip().strip(":")] = index

    current_line = 0
    while current_line < len(lines):
        line = lines[current_line].strip()
        line = line.split(" ")
        for x in range(len(line)):
            line[x] = line[x].strip(",")

        instruction = line[0]
        if instruction == "addi":
            rd, rs, immediate = line[1], line[2], line[3]
            registers[rd] = registers[rs] + int(immediate)
        elif instruction == "sw":
            rs = line[1]
            offset, rd = line[2].split("(")
            rd = rd.strip(")")
            memory_locations[registers[rd] + int(offset)] = registers[rs]
        elif instruction == "div":
            rs, rt = line[1], line[2]
            registers["lo"] = registers[rs] // registers[rt]
            registers["hi"] = registers[rs] % registers[rt]
        elif instruction == "mfhi":
            rd = line[1]
            registers[rd] = registers["hi"]
        elif instruction == "beq":
            rs, rt, label = line[1], line[2], line[3]
            if registers[rs] == registers[rt]:
                current_line = labels[label] - 2
        elif instruction == "add":
            rd, rs, rt = line[1], line[2], line[3]
            registers[rd] = registers[rs] + registers[rt]
        elif instruction == "syscall":
            call_type = registers["$v0"]
            value = registers["$a0"]
            if call_type == 1:
                print(value, end="")
            elif call_type == 4:
                char = -1
                while char != 0:
                    char = memory_locations[registers["$gp"] + value]
                    if not char == 0:
                        print(chr(char), end="")
                    value += 4
            elif call_type == 10:
                break
            elif call_type == 11:
                print(chr(value), end="")
        elif instruction == "slt":
            rd, rs, rt = line[1], line[2], line[3]
            if rs < rt:
                registers[rd] = 1
            else:
                registers[rd] = 0
        print(line)
        current_line += 1


def simulate(input_file):
    extension = input_file.split(".")[1]
    mips_file = None
    if extension == "txt":
        pass  # Disassemble
    elif extension == "asm" or extension == "mips":
        mips_file = open(input_file, "r")
    handle_lines(mips_file.readlines())

simulate("disassembler_output.asm")
