
def handle_lines(lines: list[str]):
    for line in lines:
        print(line, end="")

def simulate(input_file):
    extension = input_file.split(".")[1]
    mips_file = None
    if extension == "txt":
        pass  # Disassemble
    elif extension == "asm" or extension == "mips":
        mips_file = open(input_file, "r")

    handle_lines(mips_file.readlines())

simulate("fizzbuzz.asm")
