# variable declaration is automatic
memoryAddress = 0x10007FFC  # global pointer default value minus 4 (higher addresses will be used to store strings, lower for vars)
tRegister = 0
# create empty dictionary called vars (hash table)
vars = {}
loop_stack = []  # Top of the stack will be the innermost loop which the function is currently executing
loop_count = 1  # Number of initialized for-loops

def initialize_variable(varName, value=None):
    # makes both global, not local (method) variables
    global memoryAddress, tRegister
    # sets register name to proper format
    tRegisterName = f"$t{tRegister}"
    # calls function ???
    setVariableRegister(varName, tRegisterName)
    # returns as appropriate string as addi with $zero (formatted)
    # put f in front of string, and use {} for variables
    returnText = f"addi {tRegisterName}, $zero, {memoryAddress}\n"
    # increase register value and memory address
    tRegister += 1
    memoryAddress -= 4
    if value is not None:
        returnText += getAssignmentLinesImmediateValue(value, varName)
    return returnText

# saves each variable name to a register using dictionary
def setVariableRegister(varName, tRegister):
    global vars
    # uses dictionary (vars), varName is key and tRegister is the value
    vars[varName] = tRegister

# gets register based on variable name
def getVariableRegister(varName):
    global vars
    # if key found in dictionary, return value
    if varName in vars:
        return vars[varName]
    else:
        return "ERROR"


def getAssignmentLinesImmediateValue(val, varName):
    global tRegister
    outputText = (f"addi $t{tRegister}, $zero, {val}\n"
                  f"sw $t{tRegister}, 0({getVariableRegister(varName)})\n")
    return outputText


def getAssignmentLinesVariable(varSource, varDest):
    global tRegister
    outputText = ""
    registerSource = getVariableRegister(varSource)
    outputText += f"lw $t{tRegister}, 0({registerSource})" + "\n"
    registerDest = getVariableRegister(varDest)
    outputText += f"sw $t{tRegister}, 0({registerDest})"
    # tRegister += 1
    return outputText


def compile(c_file: str, mips_file: str):
    global loop_count
    global loop_stack
    # open and read c file
    f = open(c_file, "r")
    lines = f.readlines()
    output_lines = []
    outputText = ""
    for line in lines:
        line = line.strip()
        current_line = len(output_lines)
        print(current_line)
        if line.startswith("for"):
            parts = line[5:].split(";")
            assignment = parts[0].split(" ")
            outputText += initialize_variable(assignment[1], assignment[3])
            outputText += f"loop{loop_count}:\n"
            loop_stack.append(f"loop{loop_count}")
            loop_count += 1
        elif "if" in line:
            _, expr = line.split("if ")
            expr = expr.replace("(","").replace(")","").replace("{","").replace("\n", "")
            expr = expr.split("&&")
            output_lines.append(expr)
            print(expr)

        elif line.startswith("}"):
            outputText += "AFTER:" + "\n"

        # int declarations
        elif line.startswith("int "):
            if "(" in line and ")" in line:
                _, label = line.split()
                label = label.replace("(", "").replace(")", "").replace("{", "")
                outputText += label + ":\n"
            else:
                _, var = line.split()
                var = var.strip(";")
                outputText += initialize_variable(var)

        # assignments
        elif "=" in line:
            varName, _, val = line.split()
            val = val.strip(";")

            if val.isdigit():
                # immediate value assignments
                outputText += getAssignmentLinesImmediateValue(val, varName)
            else:
                # variable assignments
                outputText += getAssignmentLinesVariable(val, varName) + "\n"

        else:
            pass

    # write output to output file
    outputFile = open(mips_file, "w")
    outputFile.write(outputText)


if __name__ == "__main__":
    compile("program7.c", "output7.asm")