# variable declaration is automatic
memoryAddress = 0x10007FFC  # global pointer default value minus 4 (higher addresses will be used to store strings, lower for vars)
tRegister = 0
# create empty dictionary called vars (hash table)
vars = {}
loops = {}
loop_count = 0  # Number of initialized for-loops
loop_stack = []
conditional_count = 0  # Number of conditional statements
conditional_tree_count = 0
conditional_stack = []
conditionals = {}
string_count = 0

def initialize_variable(varName, value=None):
    # makes both global, not local (method) variables
    global memoryAddress, tRegister
    # sets register name to proper format
    tRegisterName = f"$t{tRegister}"
    # calls function ???
    setVariableRegister(varName, tRegisterName)
    # returns as appropriate string as addi with $zero (formatted)
    # put f in front of string, and use {} for variables
    returnText = f"li {tRegisterName}, {memoryAddress}\n"
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
    outputText = (f"li $t{tRegister}, {val}\n"
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
    loop_stack.insert(0, f"loop{loop_count}")
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


def simplify_operands(expression):
    global tRegister
    output = []
    left = expression[0].strip()
    right = expression[1].strip()
    left = left.split(" ")
    if len(left) == 1:  # If left is an expression in and of itself, eval and put the result in tRegister
        if left[0].isnumeric():
            output.append(f"li $t{tRegister + 1}, {right[0]}\n")
        else:
            output.append(f"lw $t{tRegister}, 0({vars[left[0]]})\n")
    else:
        if left[1] == "%":
            if left[2].isnumeric():
                output.append(f"li $t{tRegister}, {left[2]}\n")
            else:
                output.append(f"lw $t{tRegister + 1}, 0({vars[left[2]]})\n")
                output.append(f"add $t{tRegister}, $zero, $t{tRegister + 1}\n")
            output.append(f"lw $t{tRegister + 1}, 0({vars[left[0]]})\n")
            output.append(f"div $t{tRegister + 1}, $t{tRegister}\n")
            output.append(f"mfhi $t{tRegister}\n")
    right = right.split(" ")
    if len(right) == 1:  # Same deal
        if right[0].isnumeric():
            output.append(f"li $t{tRegister + 1}, {right[0]}\n")
        else:
            output.append(f"lw $t{tRegister + 1}, 0({vars[right[0]]})\n")
    return output


def check_condition(statement: str):
    global tRegister
    statement = statement.strip()
    operators = ["==", "<="]
    for op in operators:
        if op in statement:
            statement = statement.split(op)

            output = simplify_operands(statement)  # tRegister and # tRegister + 1 will contain the operands
            if op == "==":
                output.append(f"bne $t{tRegister}, $t{tRegister + 1}, skip{conditional_count}\n")
            elif op == "<=":
                output.append(f"ble $t{tRegister}, $t{tRegister + 1}, skip{conditional_count}\n")
            return output


def insert_string(string, op_lines):
    global string_count
    if not op_lines[0].startswith(".data"):
        op_lines.insert(0, ".data\n")
        op_lines.insert(1, f"string{string_count}: .asciiz \"{string}\"\n")
        op_lines.insert(2, ".text\n")
    else:
        op_lines.insert(1, f"string{string_count}: .asciiz \"{string}\"\n")


def compile(c_file: str, mips_file: str):
    global conditional_count, conditional_tree_count, loop_count, loop_stack, loops, string_count
    # open and read c file
    f = open(c_file, "r")
    lines = f.readlines()
    output_lines = []
    end_offset = 0  # The offset from the end at which to insert new lines, used for loops and such
    for line in lines:
        line = line.split("//")[0]
        line = line.strip()
        if line is None:
            continue
        if loop_stack:
            if "{" in line:
                loops[loop_stack[0]] += 1
            elif "}" in line:
                loops[loop_stack[0]] -= 1
        if conditional_stack:
            print(conditional_stack[0])
            print(conditionals[conditional_stack[0]])
            print(line)

            if "}" in line:
                print("zing")
                conditionals[conditional_stack[0]] -= 1

                if conditionals[conditional_stack[0]] == 0:
                    print("zam")
                    print(conditional_stack)
                    conditional_stack.pop(0)
                    end_offset -= 1
            elif "{" in line:
                conditionals[conditional_stack[0]] += 1

        if line.startswith("for"):
            parts = line[5:].split(";")
            add_to_output(initialize_for_loop(parts[0].strip(), parts[1].strip(), parts[2].strip()), output_lines, end_offset)
            end_offset += 5
            loop_count += 1
        elif "if" in line:
            if line.strip("}").strip().startswith("else"):
                add_to_output(f"j endloop{loop_count - 1}\n", output_lines, end_offset + 1)  # Temp & only works if the ifs are within a loop, try to fix it
            _, expr = line.split("if ")
            expr = expr.replace("(","").replace(")","").replace("{","").replace("\n", "")
            expr = expr.split("&&")
            for e in expr:
                add_to_output(check_condition(e), output_lines, end_offset)
            add_to_output(f"skip{conditional_count}:\n", output_lines, end_offset)
            conditionals[f"skip{conditional_count}"] = 1
            conditional_stack.insert(0, f"skip{conditional_count}")
            conditional_count += 1
            end_offset += 1
        elif line.startswith("printf"):
            line = line.split("\"")
            printable, v = line[1], line[2]
            v = v.strip(",").strip().strip(";").strip(")").split(",")
            v = [val.strip() for val in v]
            if "%d" in printable:
                printable = printable.split("%d")
                for i in range(len(printable) - 1):
                    if printable[i] != "":
                        insert_string(printable[i], output_lines)
                        add_to_output(["li $v0, 4\n", f"la $a0, string{string_count}\n", "syscall\n"], output_lines, end_offset)
                        string_count += 1
                    add_to_output(["li $v0, 1\n", f"lw $t{tRegister}, 0({vars[v[i]]})\n", f"move $a0, $t{tRegister}\n", "syscall\n"], output_lines, end_offset)
                if printable[len(printable) - 1] != "":
                    insert_string(printable[len(printable) - 1], output_lines)
                    add_to_output(["li $v0, 4\n", f"la $a0, string{string_count}\n", "syscall\n"], output_lines,
                                  end_offset)
                    string_count += 1
            else:
                insert_string(printable, output_lines)
                add_to_output(["li $v0, 4\n", f"la $a0, string{string_count}\n", "syscall\n"], output_lines, end_offset)
                string_count += 1
        elif line.startswith("}"):
            if loop_stack and loops[loop_stack[0]] == 0:  # Matching open and closed curly braces (loop over)
                loop_stack.pop(0)
                end_offset -= 5
            if conditional_stack and conditionals[conditional_stack[0]] == 0:
                conditional_stack.pop(0)
                end_offset -= 1

        # int declarations
        elif line.startswith("int "):
            if "(" in line and ")" in line:
                label = line.split()[1]
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