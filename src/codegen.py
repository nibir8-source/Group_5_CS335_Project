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
                offset = 8 + paramSize - \
                    self.helper.symbolTables[identScope].table[ident]['size'] - \
                    self.helper.symbolTables[identScope].table[ident]['offset']
            else:
                offset = 8 + paramSize - \
                    self.helper.symbolTables[identScope].table[ident]['offset']

        else:
            if 'parent' in self.helper.symbolTables[identScope].table[ident]:
                # parent = self.helper.symbolTables[identScope].table[ident]['parent']
                # parentScope = self.helper.symbolTables[identScope].table[ident]['parentScope']
                offset = self.helper.symbolTables[identScope].table[ident]['offset']
            else:
                offset = -(self.helper.symbolTables[identScope].table[ident]['offset'] +
                        self.helper.symbolTables[identScope].table[ident]['size'] - paramSize)
        if offset >= 0:
            return '+'+str(offset)
        return str(offset)


    def addFunc(self, name):
        funcScope = self.helper.symbolTables[0].functions[name]

        # add function label
        self.asmCode.append(name+':')

        # standard prologue
        self.add_prologue()

        # update stack pointer to store all the varaibles(except parameters) in current sym table
        self.asmCode.append('sub esp, '+str(helper.getWidth(funcScope) -
                            helper.getParamWidth(funcScope) + helper.getLargest(funcScope)))

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
                    retValOffset = self.ebpOffset(
                        self.code[self.codeIndex][1], self.scopeInfo[self.codeIndex][1], funcScope)
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

    def setFlags(self, instr, scopeInfo):
        flag = [0 for x in instr]
        for i in range(1, len(instr)):
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
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], edi')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], edi')
        return code

    def genCode(self, idx, funcScope):
        # Check instruction type and call function accordingly
        instr = self.code[idx]
        scopeInfo = self.scopeInfo[idx]

        if instr[0] == 'return':
            return []
        elif len(instr) == 1:
            return [instr[0]+':']
        elif instr[0] == '+int':
            return self.add_op(instr, scopeInfo, funcScope)
        elif instr[0] == '+float':
            return self.fadd_op(instr, scopeInfo, funcScope)
        elif instr[0] == '-float':
            if len(instr) == 4:
                return self.fsub_op(instr, scopeInfo, funcScope)
            else:
                return self.unary_fminus(instr, scopeInfo, funcScope)
        if instr[0] == '-int':
            if len(instr) == 4:
                return self.sub_op(instr, scopeInfo, funcScope)
            else:
                return self.unary_minus(instr, scopeInfo, funcScope)
        if instr[0] == '*int':
            return self.mul_op(instr, scopeInfo, funcScope)
        if instr[0] == '*float':
            return self.fmul_op(instr, scopeInfo, funcScope)
        if instr[0] == '/int':
            return self.div_op(instr, scopeInfo, funcScope)
        if instr[0] == '/float':
            return self.fdiv_op(instr, scopeInfo, funcScope)

        if instr[0] == '=':
            return self.assign_op(instr, scopeInfo, funcScope)
        if instr[0] == '+=':
            return self.add_assign_op(instr, scopeInfo, funcScope)
        if instr[0] == '-=':
            return self.sub_assign_op(instr, scopeInfo, funcScope)
        if instr[0] == '*=':
            return self.mul_assign_op(instr, scopeInfo, funcScope)
        if instr[0] == '/=':
            return self.div_assign_op(instr, scopeInfo, funcScope)

        if instr[0] == 'retval':
            return self.getRetVal(instr, scopeInfo, funcScope)

        if instr[0] in self.relops:
            return self.relops_cmp(instr, scopeInfo, funcScope)

        if instr[0] in self.frelops:
            return self.relops_fcmp(instr, scopeInfo, funcScope)

        if instr[0] == 'if':
            return self.if_op(instr, scopeInfo, funcScope)
        if instr[0] == 'goto':
            return self.goto_op(instr, scopeInfo, funcScope)

        if instr[0] in [ '||' , '&&']:
            return self.logical(instr, scopeInfo, funcScope)

        if instr[0] in ['--', '++']:
            return self.inc_dec(instr, scopeInfo, funcScope)

        if instr[0] == 'print_int':
            return self.print_int(instr, scopeInfo, funcScope)
        if instr[0] == 'print_float':
            return self.print_float(instr, scopeInfo, funcScope)
        if instr[0] == 'print_string':
            return self.print_string(instr, scopeInfo, funcScope)
        elif instr[0] == 'scan_int':
            return self.scan_int(instr, scopeInfo, funcScope)
        elif instr[0] == 'scan_string':
            return self.scan_string(instr, scopeInfo, funcScope)
        elif instr[0] == 'param':
            return self.param(instr, scopeInfo, funcScope)
        elif instr[0] == 'call':
            # function call
            return ['call '+instr[1]]

        if instr[0] == '*pointer':
            return self.assign_ptr_rhs(instr, scopeInfo, funcScope)
        if instr[0][0] == '&':
            return self.ampersand_op(instr, scopeInfo, funcScope)

    def getCode(self):
        while True:
            if self.codeIndex >= len(self.code):
                break
            funcName = self.code[self.codeIndex][0].split(':')
            self.addFunc(funcName[0])
        return self.asmCode

if __name__ == '__main__':
    # Load files
    # rootNode = pkl.load(open('rootNode.p', 'rb'))
    # assert(len(rootNode.code) == len(rootNode.scopeInfo))
    # helper = pkl.load(open('helper.p', 'rb'))

    codeGen = CodeGenerator(rootNode, scopeTab)

    outfile = open('assembly.asm', 'w')
    x86Code = codeGen.getCode()

    for code_ in x86Code:
        if code_.split(' ')[0] in ['global', 'section', 'extern']:
            outfile.write(code_ + '\n')
        elif code_[-1:] == ':' and 'main' in code_:
            outfile.write('main:\n')
        elif code_[-1:] == ':':
            outfile.write(code_ + '\n')
        else:
            outfile.write('    '+code_+'\n')
    outfile.close()
