import re

# paterns
labelPattern = "[\s]*\(([\w]+)\)[\s]*[//]?[\w\s]*"
#labelPatern = "[\s]*\(([\w]+)\)[\s]*[[#][\w\s]*]*" //todo fix and replace
regularCcodeLine = "[\s]*([^[//\(\)\s]*)"
AcodePattern = '@([\w]*)'
commentPattern = '\A\s*//'

# tables
symbol_table = {}
jump_dictionary = {"JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100",
                   "JNE":"101", "JLE":"110", "JMP":"111"}
comp_dictionary = {"0":"101010", "1":"111111", "-1":"111010", "D":"001100",
                   "A":"110000", "M":"110000", "!D":"001101", "!A":"110001",
                   "!M":"110001", "-D":"001111", "-A":"110011", "-M":"110011",
                   "D+1":"011111", "A+1":"110111", "M+1":"110111",
                   "D-1":"001110", "A-1":"110010", "M-1":"110010",
                   "D+A":"000010", "D+M":"000010", "D-A":"010011",
                   "D-M":"010011", "A-D":"000111", "M-D":"000111",
                   "D&A":"000000", "D&M":"000000", "D|A":"010101",
                   "D|M":"010101",
                   # Todo Carmel, i added the RX keys.
                   "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5,
                   "R6": 6, "R7": 7, "R8": 8, "R9": 9,
                   "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14,
                   "R15": 15}
TRUE = "1"
FALSE = "0"


def merge_dicts(*dict_args):
    ''' Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts. '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def initialize():
    '''
    sets the initialize dictionaries.
    '''
    global symbol_table
    symbol_table = merge_dicts(jump_dictionary, comp_dictionary)
    return


def main(file_name):
    '''
    manage the sequence of the program.
    :param file_name: the given file name
    '''
    initialize()
    label_processor(file_name)
    var_processor()
    parser(file_name)
    return  # todo - what do we need to return?


def label_processor(file_name):
    '''
    create a temporary new asm file ("tempFile.asm") with no labels, comments
    or empty lines.
    :param file_name: the given file name
    '''
    tempAsmFile = open("tempFile.asm", 'w')
    counter = -1
    global symbol_table
    with open(file_name, 'rU') as f:
        for line in f:
            if line != '\n':
                isCommentLine = re.search(commentPattern, line)
                if isCommentLine:
                    continue
                counter += 1
                result = re.search(labelPattern, line)
                if result:
                    label = result.group(1)
                    if label:
                        symbol_table[label] = counter
                        counter -=1
                else:
                    result = re.search(regularCcodeLine, line)
                    if result:
                        cleanLine = result.group(1)
                        if cleanLine and cleanLine != "\n":
                            tempAsmFile.write(cleanLine + "\n")
    tempAsmFile.close()
    return


def var_processor():
    '''
    create a temporary new asm file ("tempVarFile.asm") with no variables as well.
    '''
    variableCounter = 16
    tempAsmVarFile = open("tempVarFile.asm", 'w')
    global symbol_table
    with open('tempFile.asm', 'rU') as f:
        for line in f:
            result = re.search(AcodePattern, line)
            if result:
                variable = result.group(1)
                if variable:  # there is a variable after @
                    if variable.isdigit():
                        tempAsmVarFile.write(line)
                    elif variable in symbol_table:  # @ point to a known label
                        tempAsmVarFile.write("@"+str(symbol_table[variable])+"\n")
                    else:  # @ point to a new variable
                        symbol_table[variable] = variableCounter
                        variableCounter += 1
                        tempAsmVarFile.write("@"+str(symbol_table[variable])+"\n")
            else:
                tempAsmVarFile.write(line)
    tempAsmVarFile.close()
    return


def parser(file_name):
    '''
    create the hack binary file.
    :param file_name:
    :return:
    '''
    global symbol_table
    hackFile = open(file_name + ".hack", 'w')
    with open("tempVarFile.asm", 'r') as f:
        for line in f:
            if line[0] == '@':
                hackFile.write(codeAcode(line))
            else:
                hackFile.write(codeCcode(line))
    return


def codeAcode(Acodeline):
    Acodeline = Acodeline[1:]  # todo Carmel - i add this line to your code
    Acodeline = int(Acodeline) #Acodeline as an int
    binary_rep = '{0:16b}'.format(Acodeline) #convert to binary
    binary_rep = str(binary_rep) #Acodeline is a string
    return (binary_rep.replace(" ", "0")) #replace all the spaces in 0 and return


def codeCcode(Ccodeline): # example: d=d+1;jmp
    Ccodeline = Ccodeline[1:] # todo Carmel - i add this line to your code
    CcodeArray = Ccodeline.split(";") # CcodeArray[0]=dest&comp, CcodeArray[1]=jump
    binaric_jump = "000" # defualt jump instruction, in case there is no jump
    if (len(CcodeArray)==2):
        binaric_jump = codeJumpInstruction(CcodeArray[1])
    destCompArray = CcodeArray[0].split("=") # destCompArray[0]=dest, destCompArray[1]=comp
    binaric_dest = codeDestInstruction(destCompArray[0])
    binaric_comp = codeCompInstruction(destCompArray[1])
    defult_c_code = "111"
    binaric_c_command = defult_c_code+binaric_comp+binaric_dest+binaric_jump
    return binaric_c_command


def codeJumpInstruction(jump_to_code):
    return jump_dictionary[jump_to_code]


def codeDestInstruction(dest_to_code):  ### DECIDED TO DO IT IN DICTIONARY
    dest_code_array = [FALSE,FALSE,FALSE]
    if "M" in dest_to_code:
        dest_code_array[2] = TRUE
    if "D" in dest_to_code:
        dest_code_array[1] = TRUE
    if "A" in dest_to_code:
        dest_code_array[0] = TRUE
    binaric_dest = "".join(dest_code_array)
    return binaric_dest


def codeCompInstruction(comp_to_code):
    a=FALSE
    if "M" in comp_to_code:
        a = TRUE
        binaric_partial_code = comp_dictionary[comp_to_code]
    return a + binaric_partial_code


main('MaxL.asm')  # todo change in order to chek and then delete