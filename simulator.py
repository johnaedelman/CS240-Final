from Assembler.assembler import assemble_and_label
from Disassembler.disassembler import disassemble
from Compiler.compiler import compile
from random import randint


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
        # Math/bitwise operations
        if instruction == "addi":
            rd, rs, immediate = line[1], line[2], line[3]
            registers[rd] = registers[rs] + int(immediate)
        elif instruction == "div":
            rs, rt = line[1], line[2]
            registers["lo"] = registers[rs] // registers[rt]
            registers["hi"] = registers[rs] % registers[rt]
        elif instruction == "add":
            rd, rs, rt = line[1], line[2], line[3]
            registers[rd] = registers[rs] + registers[rt]
        elif instruction == "sub":
            rd, rs, rt = line[1], line[2], line[3]
            registers[rd] = registers[rs] - registers[rt]
        elif instruction == "and":
            rd, rs, rt = line[1], line[2], line[3]
            registers[rd] = registers[rs] % registers[rt]
        elif instruction == "or":
            rd, rs, rt = line[1], line[2], line[3]
            registers[rd] = registers[rs] | registers[rt]

        # Memory addresses/register manipulation
        elif instruction == "sw":
            rs = line[1]
            offset, rd = line[2].split("(")
            rd = rd.strip(")")
            memory_locations[registers[rd] + int(offset)] = registers[rs]
        elif instruction == "lw":
            rd = line[1]
            offset, rs = line[2].split("(")
            rs = rs.strip(")")
            registers[rd] = memory_locations[registers[rs] + int(offset)]
        elif instruction == "mfhi":
            rd = line[1]
            registers[rd] = registers["hi"]

        # Branching/conditionals
        elif instruction == "slt":
            rd, rs, rt = line[1], line[2], line[3]
            if registers[rs] < registers[rt]:
                registers[rd] = 1
            else:
                registers[rd] = 0
        elif instruction == "beq":
            rs, rt, label = line[1], line[2], line[3]
            if registers[rs] == registers[rt]:
                current_line = labels[label] - 1
        elif instruction == "bne":
            rs, rt, label = line[1], line[2], line[3]
            if registers[rs] != registers[rt]:
                current_line = labels[label] - 1
        elif instruction == "j":
            label = line[1]
            current_line = labels[label] - 1

        # Syscalls
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

        # Custom instructions
        elif instruction == "kill":
            rd, rs = line[1], line[2]
            registers[rd] = 0
            registers[rs] = 0
            print("You were slain...")
        elif instruction == "revive":
            rd, rs = line[1], line[2]
            registers[rd] = registers[rs] // 2
            print(f"You revived! Your health recovered to {registers[rd]}/{registers[rs]}.")
        elif instruction == "heal":
            rd, rs = line[1], line[2]
            registers[rd] = registers[rd] + 150
            registers[rs] = 60
            print(f"Drank a health potion! Your health recovered to {registers[rd]} and you gained 60 seconds of potion sickness.")
        elif instruction == "roll":
            rd, immediate = line[1], line[2]
            registers[rd] = randint(0, int(immediate))
        elif instruction == "boost":
            rd, rs = line[1], line[2]
            registers[rd] = pow(registers[rd], registers[rs])
            print(f"You got an exponential boost!! Your health rose to {registers[rd]}.")
        elif instruction == "hurt":
            rd, rs, immediate = line[1], line[2], line[3]
            registers[rd] = registers[rs] - int(immediate)
            print(f"You got hit! Your health fell to {registers[rd]}.")
        elif instruction == "hit":
            rd, rs = line[1], line[2]
            registers[rd] = registers[rs] // 2
            print(f"You hit the monster! Its health fell to {registers[rd]}.")
        elif instruction == "curse":
            rd, rs = line[1], line[2]
            registers[rd] = registers[rd] - (registers[rs] * 4)
            print(f"You've been cursed! Your health fell to {registers[rd]}.")
        elif instruction == "charge":
            rd, rs, rt = line[1], line[2], line[3]
            registers[rd] = registers[rd] - ((registers[rt] - registers[rs]) * 5)
            print(f"You used a powerful charged attack! The monster's health fell to {registers[rd]}.")
        elif instruction == "absorb":
            rd, rs, immediate = line[1], line[2], line[3]
            registers[rd] = registers[rd] + int(int(immediate) * (registers[rs] / 100))
            print(f"You absorbed {immediate}% of the monster's attack against you! Your health rose to {registers[rd]}.")
        current_line += 1


def simulate(input_file, source_type="bin"):
    default = "simulator_latest.txt"
    mips_file = None
    if source_type == "bin":
        disassemble(input_file, default)
        mips_file = open(default, "r")
    elif source_type == "asm":
        assemble_and_label(input_file, default)
        disassemble(default, default)
        mips_file = open(default, "r")
    elif source_type == "c":
        compile(input_file, default)
        assemble_and_label(default, default)
        disassemble(default, default)
        mips_file = open(default, "r")
    print("[SIMULATOR] New program simulation initializing.")
    handle_lines(mips_file.readlines())
    print("[SIMULATOR] Program simulation executed successfully.")


if __name__ == "__main__":
    while True:
        check = input("Would you like to compile, assemble, disassemble, simulate, or exit?\n")
        check = check.strip().casefold()
        if check == "compile" or check == "c":
            in_file = input("Specify a C input file path.\n")
            out_file = input("Specify an assembly output file path.\n")
            compile(in_file, out_file)
        elif check == "assemble" or check == "a":
            in_file = input("Specify an assembly input file path.\n")
            out_file = input("Specify a binary output file path.\n")
            assemble_and_label(in_file, out_file)
        elif check == "disassemble" or check == "d":
            in_file = input("Specify a binary input file path.\n")
            out_file = input("Specify an assembly output file path.\n")
            disassemble(in_file, out_file)
        elif check == "simulate" or check == "s":
            in_file = input("Specify an input file path.\n")
            bin_check = input("Is this a C (c) file, an assembly (a) file, or a binary (b) file?\n")
            bin_check = bin_check.strip().casefold()
            if bin_check == "binary" or bin_check == "bin" or bin_check == "b":
                simulate(in_file)
            elif bin_check == "assembly" or bin_check == "asm" or bin_check == "a":
                simulate(in_file, "asm")
            elif bin_check == "c":
                simulate(in_file, "c")
        elif check == "exit" or check == "e":
            break
        else:
            print("Invalid input.")
