symbol_table={}
jump_dictionary = {"JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}
comp_dictionary = {"0":"101010", "1":"111111", "-1":"111010", "D":"001100", "A":"110000", "M":"110000",
                   "!D":"001101", "!A":"110001", "!M":"110001", "-D":"001111", "-A":"110011", "-M":"110011",
                   "D+1":"011111", "A+1":"110111", "M+1":"110111", "D-1":"001110", "A-1":"110010", "M-1":"110010",
                   "D+A":"000010", "D+M":"000010", "D-A":"010011", "D-M":"010011", "A-D":"000111", "M-D":"000111",
                   "D&A":"000000", "D&M":"000000", "D|A":"010101", "D|M":"010101"}
TRUE = "1"
FALSE = "0"



def initialize():
    return

def main(file_name):
    return

def label_proccessor(file_name):
    return

def var_proccessor(file_name):
    return

def parser():
    return

def codeAcode(Acodeline):
    Acodeline = int(Acodeline) #Acodeline as an int
    binary_rep = '{0:16b}'.format(Acodeline) #convert to binary
    binary_rep = str(binary_rep) #Acodeline is a string
    return (binary_rep.replace(" ", "0")) #replace all the spaces in 0 and return


def codeCcode(Ccodeline): # example: d=d+1;jmp
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

