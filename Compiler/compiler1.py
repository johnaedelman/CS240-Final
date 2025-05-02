# variable declaration is automatic
memoryAddress = 5000
tRegister = 0
# create empty dictionary called vars (hash table)
vars = dict()


def getInstructionLine(varName):
    # makes both global, not local (method) variables
    global memoryAddress, tRegister
    # sets register name to proper format
    tRegisterName = f"$t{tRegister}"
    # calls function ???
    setVariableRegister(varName, tRegisterName)
    # returns as appropriate string as addi with $zero (formatted)
    # put f in front of string, and use {} for variables
    returnText = f"addi {tRegisterName}, $zero, {memoryAddress}"
    # increase register value and memory address
    tRegister += 1
    memoryAddress += 4
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
    outputText = f"""addi $t{tRegister}, $zero, {val}
    sw $t{tRegister}, 0({getVariableRegister(varName)})"""
    tRegister += 1
    return outputText

def getAssignmentLinesVariable(varSource, varDest):
    global tRegister
    outputText = ""
    registerSource = getVariableRegister(varSource)
    outputText += f"lw $t{tRegister}, 0({registerSource})" + "\n"
    tRegister += 1
    registerDest = getVariableRegister(varDest)
    outputText += f"sw $t{tRegister-1}, 0({registerDest})"
    # tRegister += 1
    return outputText

# open and read c file
f = open("program7.c", "r")
lines = f.readlines()
# output string
outputText = ""

for line in lines:
    if line.startswith("if "):
        _, expr = line.split("if ")
        expr = expr.replace("(","").replace(")","").replace("{","")
        outputText += expr

    elif line.startswith("}"):
        outputText += "AFTER:" + "\n"

    # int declarations
    elif line.startswith("int "):
        _, var = line.split()
        var = var.strip(";")
        outputText += getInstructionLine(var) + "\n"

    # assignments
    elif "=" in line:
        varName, _, val = line.split()
        val = val.strip(";")

        if val.isdigit():
            # immediate value assignments
            outputText += getAssignmentLinesImmediateValue(val, varName) + "\n"
        else:
            # variable assignments
            outputText += getAssignmentLinesVariable(val, varName) + "\n"
    
    else:
        pass

# write output to output file
outputFile = open("output7.asm", "w")
outputFile.write(outputText)