# variable declaration is automatic
memoryAddress = 0x10007FFC  # global pointer default value minus 4 (higher addresses will be used to store strings, lower for vars)
tRegister = 0
# create empty dictionary called vars (hash table)
vars = {}
loops = {}
loop_count = 1  # Number of initialized for-loops
loop_stack = []

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

def add_to_output(line, op_lines: list[str], offset: int):
    if isinstance(line, list):
        for l in line:
            op_lines.insert(len(op_lines) - offset, l)
    else:
        op_lines.insert(len(op_lines) - offset, line)

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
    return outputText + "\n"


def initialize_for_loop(assignment, condition, update):
    assignment = assignment.split(" ")
    output = []
    output.append(initialize_variable(assignment[1], assignment[3]))
    output.append(f"loop{loop_count}:\n")
    loops[f"loop{loop_count}"] = 1
    loop_stack.append(f"loop{loop_count}")
    output.append(f"endloop{loop_count}:\n")
    output.append(f"lw $t{tRegister}, 0({vars[assignment[1]]})\n")
    update = update.strip("{").strip(")")
    if update == "i++":
        output.append(f"addi $t{tRegister}, $t{tRegister}, 1\n")
    else:  # Supports for-loops with updates of the form i++ or i += a
        update = update.split(" ")
        output.append(f"addi $t{tRegister}, $t{tRegister}, {update[2]}\n")
    output.append(f"sw $t{tRegister}, 0({vars[assignment[1]]})\n")
    condition = condition.split(" ")
    if condition[1] == "<=":
        output.append(f"ble $t{tRegister}, {int(condition[2]) - 1}, loop{loop_count}\n")
    elif condition[1] == "<":
        output.append(f"ble $t{tRegister}, {condition[2]}, loop{loop_count}\n")
    return output


def perform_operation(operator):

def check_condition(statement: str):
    statement = statement.strip()
    operators = ["==", "<=", "<"]
    for op in operators:
        if op in statement:
            statement = statement.split(op)
            print(statement)
            left = statement[0].strip()
            right = statement[1].strip()
            if statement[0].strip


def compile(c_file: str, mips_file: str):
    global loop_count
    global loop_stack
    global loops
    # open and read c file
    f = open(c_file, "r")
    lines = f.readlines()
    output_lines = []
    end_offset = 0  # The offset from the end at which to insert new lines, used for loops and such
    for line in lines:
        line = line.strip()
        if loop_stack:
            if line[len(line) - 1] == "{":
                loops[loop_stack[0]] += 1
            elif line[len(line) - 1] == "}":
                loops[loop_stack[0]] -= 1

        if line.startswith("for"):
            parts = line[5:].split(";")
            add_to_output(initialize_for_loop(parts[0].strip(), parts[1].strip(), parts[2].strip()), output_lines, end_offset)
            end_offset += 5
            loop_count += 1
        elif "if" in line:
            _, expr = line.split("if ")
            expr = expr.replace("(","").replace(")","").replace("{","").replace("\n", "")
            expr = expr.split("&&")
            for e in expr:
                check_condition(e)

        elif line.startswith("}"):
            if loop_stack and loops[loop_stack[0]] == 0:  # Matching open and closed curly braces (loop over)
                loop_stack.pop(0)
                end_offset -= 5

        # int declarations
        elif line.startswith("int "):
            if "(" in line and ")" in line:
                _, label = line.split()
                label = label.replace("(", "").replace(")", "").replace("{", "")
                add_to_output(label + ":\n", output_lines, end_offset)
            else:
                _, var = line.split()
                var = var.strip(";")
                add_to_output(initialize_variable(var), output_lines, end_offset)

        # assignments
        elif "=" in line:
            varName, _, val = line.split()
            val = val.strip(";")
            if val.isdigit():
                # immediate value assignments
                add_to_output(getAssignmentLinesImmediateValue(val, varName), output_lines, end_offset)
            else:
                # variable assignments
                add_to_output(getAssignmentLinesVariable(val, varName), output_lines, end_offset)

        else:
            pass

    # write output to output file
    outputFile = open(mips_file, "w")
    outputFile.writelines(output_lines)
    [print(line, end="") for line in output_lines]


if __name__ == "__main__":
    compile("program7.c", "output7.asm")