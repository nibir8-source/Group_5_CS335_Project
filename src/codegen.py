import pickle as pkl
import random
import string
import struct
from data_structures import *


def binary(num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))


rootNode = pkl.load(open('Sf_node.p', 'rb'))
with open('scopeTabDump', 'rb') as handle:
    scopeTab = pkl.load(handle)
# # print(rootNode.code)
# print(scopeTab[0].table.items())
asmCode = []


class CodeGen:
    def __init__(self,):
        self.asmCode = []
        self.asmCode.append('global main')
        self.asmCode.append('extern printf')
        self.asmCode.append('extern scanf')
        self.asmCode.append('extern malloc')
        self.asmCode.append('section .data')
        self.asmCode.append('temp dq 0')
        self.asmCode.append('print_int db "%i ", 0x00')
        self.asmCode.append('farray_print db "%f ", 0x0a, 0x00')
        self.asmCode.append('print_line db "", 0x0a, 0x00')
        self.asmCode.append('scan_int db "%d", 0')
        self.dataIndex = 6
        self.codeIndex = 0
        self.asmCode.append('section .text')
        self.counter = 0
        self.scopeTab = scopeTab
        self.code = rootNode.code
        self.relops = ['==int', '!=int', '<=int', '>=int', '>int', '<int']
        self.frelops = ['==float', '!=float',
                        '<=float', '>=float', '>float', '<float']

def ebpOffset(self, ident, identScope, funcScope):
    paramSize = helper.getParamWidth(funcScope)

    offset = 0
    if 'is_arg' in self.helper.symbolTables[identScope].table[ident]:
        if 'parent' not in self.helper.symbolTables[identScope].table[ident]:
            offset = 8 + paramSize - self.helper.symbolTables[identScope].table[ident]['size'] - self.helper.symbolTables[identScope].table[ident]['offset']
        else:
            offset = 8 + paramSize - self.helper.symbolTables[identScope].table[ident]['offset']

    else:
        if 'parent' in self.helper.symbolTables[identScope].table[ident]:
            # parent = self.helper.symbolTables[identScope].table[ident]['parent']
            # parentScope = self.helper.symbolTables[identScope].table[ident]['parentScope']
            offset = self.helper.symbolTables[identScope].table[ident]['offset']
        else:
            offset = -(self.helper.symbolTables[identScope].table[ident]['offset'] + self.helper.symbolTables[identScope].table[ident]['size'] - paramSize)
    if offset >= 0:
        return '+'+str(offset)
    return str(offset)

def addFunc(self,name):
    funcScope = self.helper.symbolTables[0].functions[name]

    # add function label
    self.asmCode.append(name+':')

    # standard prologue
    self.add_prologue()

    # update stack pointer to store all the varaibles(except parameters) in current sym table
    self.asmCode.append('sub esp, '+str(helper.getWidth(funcScope) - helper.getParamWidth(funcScope) + helper.getLargest(funcScope)))

    self.codeIndex += 1
    while True:
        if self.codeIndex >= len(self.code):
            break
        curr = self.code[self.codeIndex]
        if (len(curr) == 1 and curr[0][-2:] == '::'):
            break
        code_ = self.genCode(self.codeIndex, funcScope)
        if len(code_) == 0:
            # then it should be a return statement
            if len(self.code[self.codeIndex]) != 1:
                # this represents a non void function hence return value needs to be updated in eax
                retValOffset = self.ebpOffset(self.code[self.codeIndex][1], self.scopeInfo[self.codeIndex][1], funcScope)
                self.asmCode.append('lea eax, [ebp'+str(retValOffset) + ']')
            self.add_epilogue()
        else:
            if code_[0] != 'none':
                self.asmCode += code_
        self.codeIndex += 1

    # standard epilogue
    self.add_epilogue()


def add_prologue(self):
    self.asmCode.append('push ebp')
    self.asmCode.append('mov ebp, esp')

def add_epilogue(self):
    self.asmCode.append('mov esp, ebp')
    self.asmCode.append('pop ebp')
    self.asmCode.append('ret')

def unary_minus(self, instr, scopeInfo, funcScope):
    dst = instr[1]
    src1 = instr[2]
    flag = self.setFlags(instr, scopeInfo)

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)

    code = []
    code.append('mov edi, [ebp' + str(src1Offset) + ']')
    if flag[2] == 1:
        code.append('mov edi, [edi]')
    code.append('mov esi, 0')
    code.append('sub esi, edi')
    if flag[1] == 1:
        code.append('mov esi, [ebp'+ str(dstOffset) + ']')
        code.append('mov [esi], edi')
    else:
        code.append('mov [ebp' + str(dstOffset) + '], esi')
    return code

def unary_fminus(self, instr, scopeInfo, funcScope):
    dst = instr[1]
    src1 = instr[2]
    flag = self.setFlags(instr, scopeInfo)

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)

    binaryCode = binary(float(0.0))

    code = []
    code.append('mov edi, 0b' + str(binaryCode))
    code.append('mov [ebp' + str(dstOffset) + '], edi')

    code.append('fld dword [ebp' + str(dstOffset) + ']')
    # if flag[2] == 1:
    #     code.append('mov edi, [edi]')
    # code.append('mov esi, 0')
    # code.append('sub esi, edi')
    code.append('fsub dword [ebp+' + str(src1Offset) + ']')
    # if flag[1] == 1:
    #     code.append('mov esi, [ebp'+ str(dstOffset) + ']')
    #     code.append('mov [esi], edi')
    # else:
    #     code.append('mov [ebp' + str(dstOffset) + '], esi')
    code.append('fstp dword [ebp' + str(dstOffset) + ']')
    return code

def setFlags(self, instr, scopeInfo):
    flag = [0 for x in instr]
    for i in range(1,len(instr)):
        try:
            if 'reference' in self.helper.symbolTables[scopeInfo[i]].get(instr[i]):
                flag[i] = 1
        except:
            pass
    return flag

def add_op(self, instr, scopeInfo, funcScope):

    dst = instr[1]
    src1 = instr[2]
    src2 = instr[3]
    flag = self.setFlags(instr, scopeInfo)

    info_src1 = self.helper.symbolTables[scopeInfo[2]].get(src1)

    baseType = helper.getBaseType(info_src1['type'])
    if baseType[0] == 'struct':
        objOffset = self.ebpOffset(src1, scopeInfo[2], funcScope)
        dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
        code_ = []
        if flag[2] == 1:
            code_.append('mov edx, [ebp'+str(objOffset)+']')
            # dont add ebp
        else:
            code_.append('mov edx, '+str(objOffset))
        code_.append('mov esi, ' + str(src2))
        if flag[3] == 1:
            code_.append('mov esi, [esi]')
        code_.append('add edx, esi')

        if flag[2] == 1:
            code_.append('mov esi, 0')
        else:
            code_.append('mov esi, ebp')
        code_.append('add esi, edx')
        code_.append('mov [ebp' + str(dstOffset) + '], esi')
        return code_
    elif baseType[0] == 'array':
        objOffset = self.ebpOffset(src1, scopeInfo[2], funcScope)
        dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)
        code_ = []
        if flag[2] == 1:
            code_.append('mov edx, [ebp'+str(objOffset)+']')
            # dont add ebp
        else:
            code_.append('mov edx, '+str(objOffset))
        code_.append('mov esi, [ebp'+str(src2Offset)+']')
        if flag[3] == 1:
            code_.append('mov esi, [esi]')
        code_.append('add edx, esi')

        if flag[2] == 1:
            code_.append('mov esi, 0')
        else:
            code_.append('mov esi, ebp')
        code_.append('add esi, edx')
        code_.append('mov [ebp' + str(dstOffset) + '], esi')
        return code_

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)
    if isinstance(scopeInfo[3], int):
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)

    code = []
    code.append('mov edi, [ebp' + str(src1Offset) + ']')
    if flag[2] == 1:
        code.append('mov edi, [edi]')

    if isinstance(scopeInfo[3], int):
        code.append('mov esi, [ebp' + str(src2Offset) + ']')
        if flag[3] == 1:
            code.append('mov esi, [esi]')
    else:
        code.append('mov esi, ' + str(src2))

    code.append('add edi, esi')

    if flag[1] == 1:
        code.append('mov esi, [ebp'+ str(dstOffset) + ']')
        code.append('mov [esi], edi')
    else:
        code.append('mov [ebp' + str(dstOffset) + '], edi')
    return code

def fadd_op(self, instr, scopeInfo, funcScope):

    dst = instr[1]
    src1 = instr[2]
    src2 = instr[3]

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)
    if isinstance(scopeInfo[3], int):
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)

    code = []

    code.append('fld dword [ebp' + str(src1Offset) + ']')
    if isinstance(scopeInfo[3], int):
        code.append('fadd dword [ebp' + str(src2Offset) + ']')
    else:
        binaryCode = binary(float(src2))

        code.append('mov edi, 0b' + str(binaryCode))
        code.append('mov [ebp' + str(dstOffset) + '], edi')

        # rand_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
        # self.asmCode.insert(8, str(rand_str) + ': dq ' + str(src2))
        # self.dataIndex += 1
        code.append('fadd dword [ebp' + str(dstOffset) + ']')
    # code.append('faddp')
    code.append('fstp dword [ebp' + str(dstOffset) + ']')
    return code

def sub_op(self, instr, scopeInfo, funcScope):

    dst = instr[1]
    src1 = instr[2]
    src2 = instr[3]
    flag = self.setFlags(instr, scopeInfo)

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)
    if isinstance(scopeInfo[3], int):
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)

    code = []
    code.append('mov edi, [ebp' + str(src1Offset) + ']')
    if flag[2] == 1:
        code.append('mov edi, [edi]')

    if isinstance(scopeInfo[3], int):
        code.append('mov esi, [ebp' + str(src2Offset) + ']')
        if flag[3] == 1:
            code.append('mov esi, [esi]')
    else:
        code.append('mov esi, ' + str(src2))
    code.append('sub edi, esi')

    if flag[1] == 1:
        code.append('mov esi, [ebp'+ str(dstOffset) + ']')
        code.append('mov [esi], edi')
    else:
        code.append('mov [ebp' + str(dstOffset) + '], edi')
    return code

def fsub_op(self, instr, scopeInfo, funcScope):
    # print(instr)
    dst = instr[1]
    src1 = instr[2]
    src2 = instr[3]

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)
    if isinstance(scopeInfo[3], int):
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)

    code = []

    code.append('fld dword [ebp' + str(src1Offset) + ']')
    if isinstance(scopeInfo[3], int):
        code.append('fsub dword [ebp' + str(src2Offset) + ']')
    else:
        binaryCode = binary(float(src2))

        code.append('mov edi, 0b' + str(binaryCode))
        code.append('mov [ebp' + str(dstOffset) + '], edi')

        # rand_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
        # self.asmCode.insert(8, str(rand_str) + ': dq ' + str(src2))
        # self.dataIndex += 1
        code.append('fsub dword [ebp+' + str(dstOffset) + ']')
    # code.append('fsubp')
    code.append('fstp dword [ebp' + str(dstOffset) + ']')
    return code

def mul_op(self, instr, scopeInfo, funcScope):
    dst = instr[1]
    src1 = instr[2]
    src2 = instr[3]
    flag = self.setFlags(instr, scopeInfo)

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)
    if isinstance(scopeInfo[3], int):
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)

    code = []
    code.append('mov edi, [ebp' + str(src1Offset) + ']')
    if flag[2] == 1:
        code.append('mov edi, [edi]')

    if isinstance(scopeInfo[3], int):
        code.append('mov esi, [ebp' + str(src2Offset) + ']')
        if flag[3] == 1:
            code.append('mov esi, [esi]')
    else:
        code.append('mov esi, ' + str(src2))
    code.append('imul edi, esi')

    if flag[1] == 1:
        code.append('mov esi, [ebp'+ str(dstOffset) + ']')
        code.append('mov [esi], edi')
    else:
        code.append('mov [ebp' + str(dstOffset) + '], edi')
    return code

def fmul_op(self, instr, scopeInfo, funcScope):
    dst = instr[1]
    src1 = instr[2]
    src2 = instr[3]

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)
    if isinstance(scopeInfo[3], int):
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)

    code = []
    code.append('fld dword [ebp' + str(src1Offset) + ']')
    if isinstance(scopeInfo[3], int):
        code.append('fmul dword [ebp' + str(src2Offset) + ']')
    else:
        binaryCode = binary(float(src2))

        code.append('mov edi, 0b' + str(binaryCode))
        code.append('mov [ebp' + str(dstOffset) + '], edi')

        # rand_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
        # self.asmCode.insert(8, str(rand_str) + ': dq ' + str(src2))
        # self.dataIndex += 1
        code.append('fmul dword [ebp' + str(dstOffset) + ']')
    # code.append('fmulp st1, st0')
    code.append('fstp dword [ebp' + str(dstOffset) + ']')
    return code

def div_op(self, instr, scopeInfo, funcScope):
    dst = instr[1]
    src1 = instr[2]
    src2 = instr[3]
    flag = self.setFlags(instr, scopeInfo)

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)
    if isinstance(scopeInfo[3], int):
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)

    code = []
    code.append('xor edx, edx')
    code.append('mov eax, [ebp' + str(src1Offset) + ']')
    if isinstance(scopeInfo[3], int):
        code.append('mov ebx, [ebp' + str(src2Offset) + ']')
    else:
        code.append('mov ebx, ' + str(src2))
    code.append('idiv ebx')

    if flag[1] == 1:
        code.append('mov esi, [ebp'+ str(dstOffset) + ']')
        code.append('mov [esi], eax')
    else:
        code.append('mov [ebp' + str(dstOffset) + '], eax')
    return code

def fdiv_op(self, instr, scopeInfo, funcScope):
    dst = instr[1]
    src1 = instr[2]
    src2 = instr[3]

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    src1Offset = self.ebpOffset(src1, scopeInfo[2], funcScope)
    if isinstance(scopeInfo[3], int):
        src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)

    code = []
    code.append('fld dword [ebp' + str(src1Offset) + ']')
    if isinstance(scopeInfo[3], int):
        code.append('fdiv dword [ebp' + str(src2Offset) + ']')
    else:
        binaryCode = binary(float(src2))

        code.append('mov edi, 0b' + str(binaryCode))
        code.append('mov [ebp' + str(dstOffset) + '], edi')

        # rand_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
        # self.asmCode.insert(8, str(rand_str) + ': dq ' + str(src2))
        # self.dataIndex += 1
        code.append('fdiv dword [ebp' + str(dstOffset) + ']')
    # code.append('fmulp st1, st0')
    code.append('fstp dword [ebp' + str(dstOffset) + ']')
    return code

def pointer_assign(self, instr, scopeInfo, funcScope):
    dst = instr[1][1:]
    src = instr[2]
    code = []
    instr[1] = dst
    flag = self.setFlags(instr, scopeInfo)

    dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
    srcOffset = self.ebpOffset(src, scopeInfo[2], funcScope)

    code.append('mov edi, [ebp' + srcOffset + ']')
    if flag[2] == 1:
        code.append('mov edi [edi]')
    code.append('mov esi, [ebp' + dstOffset + ']')
    if flag[1] == 1:
        code.append('mov esi, [esi]')
    code.append('mov [esi], edi')
    return code