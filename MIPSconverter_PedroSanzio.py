# Dicionários:
data_opcode = {
    'lb': '100000', 'lh': '100001', 'lwl': '100010', 'lw': '100011', 'lbu': '100100', 'lhu': '100101', 'lwr': '100110', 'sb': '101000', 'sh': '101001', 'swl': '101010', 'sw': '101011', 'swr': '101110', #fim load e store

    'add': '000000', 'addu': '000000', 'sub': '000000', 'subu': '000000', 'and': '000000', 'or': '000000', 'xor': '000000','nor': '000000', 'slt': '000000', 'sltu': '000000', #fim logica e arit sem imediato

    'addi': '001000', 'addiu': '001001', 'slti': '001010', 'sltiu': '001011', 'andi': '001100', 'ori': '001101', 'xori': '001110', 'lui': '001111', #fim logica e arit com imediato
    
    'sll': '000000', 'srl': '000000', 'sra': '000000', 'sllv': '000000', 'srlv': '000000', 'srav': '000000', #deslocamento de bits

    'mhfi': '000000', 'mthi': '000000', 'mflo': '000000', 'mtlo': '000000', 'mult': '000000', 'multu': '000000', 'div': '000000', 'divu': '000000', #mult e div

    'jr': '000000', 'jalr': '000000', #desvio - tipo R

    'bltz': '000001', 'bgez': '000001', 'bltzal': '000001', 'bgezal': '000001', 'beq': '000100', 'bne': '000101', 'blez': '000110', 'bgtz': '000111', #desvio - tipo I

    'j': '000010', 'jal': '000011' #desvio - tipo J
}

#instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)
#instr I = opcode(6) + rs(5) + rt(5) + immediate(16)
#instr J = opcode(6) + add(26)

data_functions_r = {
    'add': '100000', 'addu': '100001', 'sub': '100010', 'subu': '100011', 'and': '100100', 'or': '100101', 'xor': '100110', 'nor': '100111', 'slt': '101010', 'sltu': '101011', 'sll': '000000', 'srl': '000010', 'sra': '000011', 'sllv': '000100', 'srlv': '000110', 'srav': '000111', 'mhfi': '010000', 'mthi': '010001', 'mflo': '010010', 'mtlo': '010011', 'mult': '011000', 'multu': '011001', 'div': '011010', 'divu': '011011', 'jr': '001000', 'jalr': '001001'
}

data_registers = {
    '$zero': '00000', '$t0': '01000', '$t1': '01001', '$t2': '01010',
    '$t3': '01011', '$t4': '01100', '$t5': '01101', '$t6': '01110', '$t7': '01111', '$s0': '10000', '$s1': '10001', '$s2': '10010', '$s3': '10011', '$s4': '10100', '$s5': '10101', '$s6': '10110', '$s7': '10111'
}

def convertion(instruction):
    instruction_parts = instruction.split()
    op_code = instruction_parts[0]
    
    if op_code in ['lb', 'lh', 'lwl', 'lw', 'lbu', 'lhu', 'lwr', 'sb', 'sh', 'swl', 'sw', 'swr']:
        rt = data_registers[instruction_parts[1]]
        offset, rs = instruction_parts[2].split('(')
        offset = bin(int(offset) & 0xFFFF)[2:].zfill(16) #ao converter em python tem o 0b na frente, por isso o [2:] e o zfill é para completar os 16
        rs = data_registers[rs.replace(')', '')]
        return data_opcode[op_code] + rs + rt + offset
        #instr I = opcode(6) + rs(5) + rt(5) + offset(16)

    elif op_code in ['add', 'addu', 'sub', 'subu', 'and', 'or', 'xor', 'nor', 'slt', 'sltu']:
        rd = data_registers[instruction_parts[1]]
        rs = data_registers[instruction_parts[2]]
        rt = data_registers[instruction_parts[3]]
        shamt = '00000'
        funct = data_functions_r[op_code]
        return data_opcode[op_code] + rs + rt + rd + shamt + funct
        #instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)
    
    elif op_code in ['addi', 'addiu', 'slti', 'sltiu', 'andi', 'ori', 'xori']:
        rt = data_registers[instruction_parts[1]]
        rs = data_registers[instruction_parts[2]]
        immediate = bin(int(instruction_parts[3]) & 0xFFFF)[2:].zfill(16)
        #(immediate & 0xFFFF) garante que apenas os 16 bits menos significativos do immediate sejam usados, mesmo que seja um número negativo
        #ao converter em python tem o 0b na frente, por isso o [2:] e o zfill é para completar os 16
        return data_opcode[op_code] + rs + rt + immediate
        #instr I = opcode(6) + rs(5) + rt(5) + immediate(16)

    elif op_code == 'lui':
        rt = data_registers[instruction_parts[1]]
        rs = data_registers['$zero']
        immediate = bin(int(instruction_parts[2]) & 0xFFFF)[2:].zfill(16) #ao converter em python tem o 0b na frente, por isso o [2:] e o zfill é para completar os 16
        return data_opcode[op_code] + rs + rt + immediate
        #instr I = opcode(6) + rs(5) + rt(5) + immediate(16)

    elif op_code in ['sll', 'srl', 'sra']:
        rd = data_registers[instruction_parts[1]]
        rs = '00000'
        rt = data_registers[instruction_parts[2]]
        shamt = bin(int(instruction_parts[3]))[2:].zfill(5)
        funct = data_functions_r[op_code]
        return data_opcode[op_code] + rs + rt + rd + shamt + funct
        #instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)

    elif op_code in ['sllv', 'srlv', 'srav']:
        rd = data_registers[instruction_parts[1]]
        rs = data_registers[instruction_parts[2]]
        rt = data_registers[instruction_parts[3]]
        shamt = '00000'
        funct = data_functions_r[op_code]
        return data_opcode[op_code] + rs + rt + rd + shamt + funct
        #instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)

    elif op_code in ['mfhi', 'mflo']:
        rd = data_registers[instruction_parts[1]]
        rs = '00000'
        rt = '00000'
        shamt = '00000'
        funct = data_functions_r[op_code]
        return data_opcode[op_code] + rs + rt + rd + shamt + funct
        #instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)

    elif op_code in ['mthi', 'mtlo']:
        rd = '00000'
        rs = data_registers[instruction_parts[1]]
        rt = '00000'
        shamt = '00000'
        funct = data_functions_r[op_code]
        return data_opcode[op_code] + rs + rt + rd + shamt + funct
        #instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)

    elif op_code in ['mult', 'multu', 'div', 'divu']:
        rd = '00000'
        rs = data_registers[instruction_parts[1]]
        rt = data_registers[instruction_parts[2]]
        shamt = '00000'
        funct = data_functions_r[op_code]
        return data_opcode[op_code] + rs + rt + rd + shamt + funct
        #instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)

    elif op_code == 'jr':
        rd = '00000'
        rs = data_registers[instruction_parts[1]]
        rt = '00000'
        shamt = '00000'
        funct = data_functions_r[op_code]
        return data_opcode[op_code] + rs + rt + rd + shamt + funct
        #instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)

    elif op_code == 'jalr':
        rd = data_registers[instruction_parts[1]]
        rs = data_registers[instruction_parts[2]]
        rt = '00000'
        shamt = '00000'
        funct = data_functions_r[op_code]
        return data_opcode[op_code] + rs + rt + rd + shamt + funct
        #instr R = opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + func (6)

    elif op_code == 'bltz':
        rt = '00000'
        rs = data_registers[instruction_parts[1]]
        offset = bin(int(instruction_parts[2]) & 0xFFFF)[2:].zfill(16) 
        # Converte o imediato para 16 bits com sinal (complemento de dois)
        #ao converter em python tem o 0b na frente, por isso o [2:] e o zfill é para completar os 16
        return data_opcode[op_code] + rs + rt + offset
        #instr I = opcode(6) + rs(5) + rt(5) + offset(16)

    elif op_code == 'bgez':
        rt = '00001'
        rs = data_registers[instruction_parts[1]]
        offset = bin(int(instruction_parts[2]) & 0xFFFF)[2:].zfill(16) #ao converter em python tem o 0b na frente, por isso o [2:] e o zfill é para completar os 16
        return data_opcode[op_code] + rs + rt + offset
        #instr I = opcode(6) + rs(5) + rt(5) + offset(16)

    elif op_code == 'bltzal':
        rt = '10000'
        rs = data_registers[instruction_parts[1]]
        offset = bin(int(instruction_parts[2]) & 0xFFFF)[2:].zfill(16) #ao converter em python tem o 0b na frente, por isso o [2:] e o zfill é para completar os 16
        return data_opcode[op_code] + rs + rt + offset
        #instr I = opcode(6) + rs(5) + rt(5) + offset(16)

    elif op_code == 'bgezal':
        rt = '10001'
        rs = data_registers[instruction_parts[1]]
        offset = bin(int(instruction_parts[2]) & 0xFFFF)[2:].zfill(16) #ao converter em python tem o 0b na frente, por isso o [2:] e o zfill é para completar os 16
        return data_opcode[op_code] + rs + rt + offset
        #instr I = opcode(6) + rs(5) + rt(5) + offset(16)

    elif op_code in ['j', 'jal']:
        add = bin(int(instruction_parts[1]) & 0x3FFFFFF)[2:].zfill(26)
        return data_opcode[op_code] + add
        #instr J = opcode(6) + add(26)

    elif op_code in ['beq', 'bne']:
        rs = data_registers[instruction_parts[2]]
        rt = data_registers[instruction_parts[1]]
        offset = bin(int(instruction_parts[3]) & 0xFFFF)[2:].zfill(16)
        return data_opcode[op_code] + rs + rt + offset
        #instr I = opcode(6) + rs(5) + rt(5) + offset(16)

    elif op_code in ['blez', 'bgtz']:
        rs = data_registers[instruction_parts[1]]
        rt = '00000'
        offset = bin(int(instruction_parts[2]) & 0xFFFF)[2:].zfill(16)
        return data_opcode[op_code] + rs + rt + offset
        #instr I = opcode(6) + rs(5) + rt(5) + offset(16)

def text_generator(read_file, write_file):
    with open(read_file, 'r') as read_file, open(write_file, 'w') as write_file:
        write_file.write('Nome: ' + username + '\n')
        write_file.write('Convertido de: ' + str(read_file.name) + '\n')
        write_file.write('Resultado: ' + '\n' + '\n')
        for line in read_file:
            line = line.strip().replace(',', '')
            if line:
                binary_instruction = convertion(line)
                write_file.write(binary_instruction + '\n')

username = str(input('Digite seu nome: '))
filename = str(input('Nome do arquivo para os resultados: '))
read_file = 'arquivo_teste2.txt'
write_file = str(filename) + '.txt'
text_generator(read_file, write_file)
