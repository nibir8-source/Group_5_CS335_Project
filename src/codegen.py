import pickle as pkl
import random
import string
import struct

# from sqlalchemy import func
from data_structures import *


def binary(num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))


rootNode = pkl.load(open('Sf_node.p', 'rb'))
with open('scopeTabDump', 'rb') as handle:
    scopetab = pkl.load(handle)
# # print(rootNode.code)
# print(scopetab[0].table.items())
asmCode = []


class CodeGen:
    def __init__(self, rootnode, scopetab):
        self.asmCode = []
        self.asmCode.append('global main')
        self.asmCode.append('extern printf')
        self.asmCode.append('extern scanf')
        self.asmCode.append('extern gets')
        self.asmCode.append('extern puts')
        self.asmCode.append('extern farray_print')
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
        self.scopetab = scopetab
        self.code = rootnode.code
        self.relops = ['==int', '!=int', '<=int', '>=int', '>int', '<int']
        self.frelops = ['==float', '!=float',
                        '<=float', '>=float', '>float', '<float']

    def ebpOffset(self, ident):
        try:
            scope = self.get_scope(ident)
            # offset = self.scopetab[scope].table[ident]["offset"]
            # print(ident)
            name = self.scopetab[scope].table[ident]["type"]
            # print(name)
            if(name == "temp"):
                offset = self.scopetab[scope].table[ident]["offset"]
            else:
                offset = self.scopetab[scope].table[name]["offset"]
            if offset >= 0:
                return '-'+str(offset)
            else:
                offset = -offset
                return '+'+str(offset)
        except:
            return -1
        # return str(offset)

    def addFunc(self, name):
        funcScope = self.scopetab[0].table[name]["scope"]
        # add function label
        self.asmCode.append(name+':')

        # standard prologue
        self.add_prologue()

        get_width = self.scopetab[funcScope].table["total_size"]["type"]
        # param_width = self.scopetab[0].table[name]["total_param_size"]

        # update stack pointer to store all the varaibles(except parameters) in current sym table
        self.asmCode.append('sub esp, ' + str(get_width))

        self.codeIndex += 1
        while True:
            if self.codeIndex >= len(self.code):
                break
            # curr = self.code[self.codeIndex]
            # if (len(curr) == 1 and curr[0][-2:] == '::'):
            #     break
            code_ = self.genCode(self.codeIndex)
            if len(code_) == 0:
                # then it should be a return statement
                if len(self.code[self.codeIndex]) != 1:
                    # this represents a non void function hence return value needs to be updated in eax
                    ident_scope = 0
                    ident = self.code[self.codeIndex][1]
                    for i in range(len(scopetab.keys())):
                        if (scopetab[i].parent == funcScope):
                            flag = 0
                            for _, value in scopetab[i].table:
                                if(value["tmp"] == ident):
                                    flag = 1
                                    ident_scope = i
                                    break
                            if flag == 1:
                                break
                    retValOffset = self.ebpOffset(ident, ident_scope)
                    self.asmCode.append(
                        'lea eax, [ebp'+str(retValOffset) + ']')
                # self.add_epilogue()
                self.codeIndex += 1
                break
            else:
                if code_[0] != 'none':
                    self.asmCode += code_
            self.codeIndex += 1

        # standard epilogue
        # self.add_epilogue()

    def add_prologue(self):
        self.asmCode.append('push ebp')
        self.asmCode.append('mov ebp, esp')

    def add_epilogue(self):
        self.asmCode.append('mov esp, ebp')
        self.asmCode.append('pop ebp')
        self.asmCode.append('ret')

    # do
    def get_scope(self, ident):
        for i in range(len(self.scopetab.keys())):
            if ident in self.scopetab[i].table:
                return i
        return -1

    def get_ident_info(self, ident):
        for i in range(len(self.scopetab.keys())):
            if ident in self.scopetab[i].table:
                name = self.scopetab[i].table[ident]["type"]
                if name == 'temp':
                    return self.scopetab[i].table[ident]
                return self.scopetab[i].table[name]
        return -1

    def setFlags(self, instr):
        flag = [0 for x in instr]
        for i in range(0, len(instr)):
            try:
                scope = self.get_scope(instr[i])
                if scope != -1 and self.scopetab[scope].table[instr[i]]["type"] == ['pointer', 'int']:
                    flag[i] = 1
            except:
                pass
        return flag

    def unary_minus(self, instr):
        if instr[0] != '*':
            dst = instr[0]
            src = instr[3]
        else:
            dst = instr[1]
            src = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src) != -1:
            src1Offset = self.ebpOffset(src)

        code = []
        if self.get_ident_info(src) != -1:
            code.append('mov edi, [ebp' + str(src1Offset) + ']')
            if (instr[0] == '*' and flag[4] == 1) or (instr[0] != '*' and flag[3] == 1):
                code.append('mov edi, [edi]')
        else:
            code.append('mov edi, ' + str(src))
        code.append('mov esi, 0')
        code.append('sub esi, edi')
        if instr[0] == '*':
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], edi')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], esi')
        return code

    def unary_fminus(self, instr):
        if instr[0] != '*':
            dst = instr[0]
            src = instr[3]
        else:
            dst = instr[1]
            src = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src) != -1:
            src1Offset = self.ebpOffset(src)

        binaryCode = binary(float(0.0))

        code = []
        code.append('mov edi, 0b' + str(binaryCode))
        code.append('mov [ebp' + str(dstOffset) + '], edi')
        code.append('fld dword [ebp' + str(dstOffset) + ']')

        if self.get_ident_info(src) != -1:
            if (instr[0] == '*' and flag[4] != 1) or (instr[0] != '*' and flag[3] != 1):
                code.append('fsub dword [ebp+' + str(src1Offset) + ']')
            else:
                code.append('mov edi [ebp' + str(src1Offset) + ']')
                code.append('mov edi, [edi]')
                code.append('mov esi, [ebp-4]')
                code.append('mov [ebp-4], edi')
                code.append('fsub dword [ebp-4]')
                code.append('mov [ebp-4], esi')
        else:
            bin_code = binary(float(src))
            code.append('mov edi, 0b' + str(bin_code))
            code.append('mov esi, [ebp-4]')
            code.append('mov [ebp-4], edi')
            code.append('fsub dword [ebp-4]')
            code.append('mov [ebp-4], esi')
        if flag[1] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('fstp dword [esi]')
        else:
            code.append('fstp dword [ebp' + str(dstOffset) + ']')
        return code

    def add_op(self, instr):

        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        # baseType = helper.getBaseType(info_src1['type'])
        # if baseType[0] == 'struct':
        #     objOffset = self.ebpOffset(src1, scopeInfo[2], funcScope)
        #     dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
        #     code_ = []
        #     if flag[2] == 1:
        #         code_.append('mov edx, [ebp'+str(objOffset)+']')
        #         # dont add ebp
        #     else:
        #         code_.append('mov edx, '+str(objOffset))
        #     code_.append('mov esi, ' + str(src2))
        #     if flag[3] == 1:
        #         code_.append('mov esi, [esi]')
        #     code_.append('add edx, esi')

        #     if flag[2] == 1:
        #         code_.append('mov esi, 0')
        #     else:
        #         code_.append('mov esi, ebp')
        #     code_.append('add esi, edx')
        #     code_.append('mov [ebp' + str(dstOffset) + '], esi')
        #     return code_
        # elif baseType[0] == 'array':
        #     objOffset = self.ebpOffset(src1, scopeInfo[2], funcScope)
        #     dstOffset = self.ebpOffset(dst, scopeInfo[1], funcScope)
        #     src2Offset = self.ebpOffset(src2, scopeInfo[3], funcScope)
        #     code_ = []
        #     if flag[2] == 1:
        #         code_.append('mov edx, [ebp'+str(objOffset)+']')
        #         # dont add ebp
        #     else:
        #         code_.append('mov edx, '+str(objOffset))
        #     code_.append('mov esi, [ebp'+str(src2Offset)+']')
        #     if flag[3] == 1:
        #         code_.append('mov esi, [esi]')
        #     code_.append('add edx, esi')

        #     if flag[2] == 1:
        #         code_.append('mov esi, 0')
        #     else:
        #         code_.append('mov esi, ebp')
        #     code_.append('add esi, edx')
        #     code_.append('mov [ebp' + str(dstOffset) + '], esi')
        #     return code_

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            code.append('mov edi, [ebp' + str(src1Offset) + ']')
            if flag[2] == 1:
                code.append('mov edi, [edi]')
        else:
            code.append('mov edi, ' + str(src1))

        if self.get_ident_info(src2) != -1:
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

    def fadd_op(self, instr):

        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            code.append('fld dword [ebp' + str(src1Offset) + ']')
        else:
            binaryCode = binary(float(src1))

            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov [ebp' + str(dstOffset) + '], edi')

            code.append('fld dword [ebp' + str(dstOffset) + ']')

        if self.get_ident_info(src2) != -1:
            code.append('fadd dword [ebp' + str(src2Offset) + ']')
        else:
            binaryCode = binary(float(src2))

            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov [ebp' + str(dstOffset) + '], edi')

            code.append('fadd dword [ebp' + str(dstOffset) + ']')
        code.append('fstp dword [ebp' + str(dstOffset) + ']')
        return code

    def sub_op(self, instr):

        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            if instr[3] == '-int':
                code.append('mov edi, [ebp' + str(src1Offset) + ']')
            else:
                code.append('lea edi, [ebp' + str(src1Offset) + ']')
            if flag[2] == 1:
                code.append('mov edi, [edi]')
        else:
            code.append('mov edi, ' + str(src1))

        if self.get_ident_info(src2) != -1:
            code.append('mov esi, [ebp' + str(src2Offset) + ']')
            if flag[3] == 1:
                code.append('mov esi, [esi]')
        else:
            code.append('mov esi, ' + str(src2))

        code.append('sub edi, esi')

        if flag[1] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], edi')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], edi')
        return code

    def fsub_op(self, instr):

        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            code.append('fld dword [ebp' + str(src1Offset) + ']')
        else:
            binaryCode = binary(float(src1))

            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov [ebp' + str(dstOffset) + '], edi')

            code.append('fld dword [ebp' + str(dstOffset) + ']')

        if self.get_ident_info(src2) != -1:
            code.append('fsub dword [ebp' + str(src2Offset) + ']')
        else:
            binaryCode = binary(float(src2))

            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov [ebp' + str(dstOffset) + '], edi')

            code.append('fsub dword [ebp' + str(dstOffset) + ']')
        code.append('fstp dword [ebp' + str(dstOffset) + ']')
        return code

    def mul_op(self, instr):

        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            code.append('mov edi, [ebp' + str(src1Offset) + ']')
            if flag[2] == 1:
                code.append('mov edi, [edi]')
        else:
            code.append('mov edi, ' + str(src1))

        if self.get_ident_info(src2) != -1:
            code.append('mov esi, [ebp' + str(src2Offset) + ']')
            if flag[3] == 1:
                code.append('mov esi, [esi]')
        else:
            code.append('mov esi, ' + str(src2))

        code.append('imul edi, esi')

        if flag[1] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], edi')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], edi')
        return code

    def fmul_op(self, instr):

        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            code.append('fld dword [ebp' + str(src1Offset) + ']')
        else:
            binaryCode = binary(float(src1))

            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov [ebp' + str(dstOffset) + '], edi')

            code.append('fld dword [ebp' + str(dstOffset) + ']')

        if self.get_ident_info(src2) != -1:
            code.append('fmul dword [ebp' + str(src2Offset) + ']')
        else:
            binaryCode = binary(float(src2))

            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov [ebp' + str(dstOffset) + '], edi')

            code.append('fmul dword [ebp' + str(dstOffset) + ']')
        code.append('fstp dword [ebp' + str(dstOffset) + ']')
        return code

    def div_op(self, instr):
        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1):
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        code.append('xor edx, edx')
        if self.get_ident_info(src1) != -1:
            code.append('mov eax, [ebp' + str(src1Offset) + ']')
        else:
            code.append('mov eax, ' + str(src1))

        if self.get_ident_info(src2) != -1:
            code.append('mov ebx, [ebp' + str(src2Offset) + ']')
        else:
            code.append('mov ebx, ' + str(src2))
        code.append('idiv ebx')

        if flag[1] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], eax')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], eax')
        return code

    def fdiv_op(self, instr):

        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            code.append('fld dword [ebp' + str(src1Offset) + ']')
        else:
            binaryCode = binary(float(src1))

            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov [ebp' + str(dstOffset) + '], edi')

            code.append('fld dword [ebp' + str(dstOffset) + ']')

        if self.get_ident_info(src2) != -1:
            code.append('fdiv dword [ebp' + str(src2Offset) + ']')
        else:
            binaryCode = binary(float(src2))

            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov [ebp' + str(dstOffset) + '], edi')

            code.append('fdiv dword [ebp' + str(dstOffset) + ']')
        code.append('fstp dword [ebp' + str(dstOffset) + ']')
        return code

    def pointer_assign(self, instr):
        if len(instr) == 4 and instr[2] == '*':
            dst = instr[0]
            src = instr[3]
            dstOffset = self.ebpOffset(dst)
            srcOffset = self.ebpOffset(src)
            code = []
            code.append('mov edi, [ebp' + str(srcOffset) + ']')
            code.append('mov edi, [edi]')
            code.append('mov [ebp' + str(dstOffset) + '], edi')
            return code
        else:
            dst = instr[1]
            src = instr[3]
            code = []

            dstOffset = self.ebpOffset(dst)
            if self.get_ident_info(src) != -1:
                srcOffset = self.ebpOffset(src)
                code.append('mov edi, [ebp' + srcOffset + ']')
            else:
                code.append('mov edi, ' + str(src))
            code.append('mov esi, [ebp' + dstOffset + ']')
            # code.append('mov esi, [esi]')
            code.append('mov [esi], edi')
        return code

    def assign_op(self, instr):

        dst = instr[0]
        src = instr[2]
        code = []
        flag = self.setFlags(instr)

        if dst[0] == '*' or (len(instr) == 4 and instr[2] == '*'):
            return self.pointer_assign(instr)

        # s1 = self.get_scope(instr[0])
        # s2 = self.get_scope(instr[2])
        dst_info = self.get_ident_info(dst)
        src_info = self.get_ident_info(src)

        baseType = dst_info["type"]
        #baseType = helper.getBaseType(data_['type'])

        if baseType[0] in ['struct', 'array']:
            offset1 = self.ebpOffset(instr[0])
            offset2 = self.ebpOffset(instr[2])

            self.counter += 1
            label = 'looping' + str(self.counter)
            iters = int(dst_info['size'] / 4)
            code_ = ['mov esi, ebp', 'mov ebx, ebp']
            code_.append('add esi, '+offset1)
            code_.append('add ebx, '+offset2)
            if flag[2] == 1:
                code_.append('mov ebx, [ebp' + offset2 + ']')
            if flag[0] == 1:
                code_.append('mov esi, [ebp' + offset1 + ']')
            code_.append('mov cx, '+str(iters))
            code_.append(label + ':')
            code_.append('mov edx, [ebx]')
            code_.append('mov [esi], edx')
            code_.append('add esi, 4')
            code_.append('add ebx, 4')
            code_.append('dec cx')
            code_.append('jnz '+label)
            return code_
        if baseType == ['float']:
            if src_info != -1:
                dstOffset = self.ebpOffset(dst)
                srcOffset = self.ebpOffset(src)
                code.append('fld dword [ebp' + srcOffset + ']')
                code.append('fstp dword [ebp' + dstOffset + ']')
            else:
                dstOffset = self.ebpOffset(dst)

                binaryCode = binary(float(src))
                code.append('mov edi, 0b' + str(binaryCode))
                code.append('mov [ebp' + dstOffset + '], edi')
        else:
            if src_info != -1:
                dstOffset = self.ebpOffset(dst)
                srcOffset = self.ebpOffset(src)
                code.append('mov edi, [ebp' + srcOffset + ']')
                if flag[2] == 1:
                    code.append('mov edi, [edi]')
                if flag[1] == 1:
                    code.append('mov esi, [ebp' + str(dstOffset) + ']')
                    code.append('mov [esi], edi')
                else:
                    code.append('mov [ebp' + str(dstOffset) + '], edi')
            else:
                dstOffset = self.ebpOffset(dst)
                if src[:-1] == 'retval_':
                    code.append('mov edi, eax')
                else:
                    code.append('mov edi, ' + str(src))
                if flag[1] == 1:
                    code.append('mov esi, [ebp' + str(dstOffset) + ']')
                    code.append('mov [esi], edi')
                else:
                    code.append('mov [ebp' + str(dstOffset) + '], edi')

        return code

    def assign_op_ptr(self, instr):
        dst = instr[0][1:]
        src = instr[2]
        # *t1 += t2
        code = []
        instr[0] = dst
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        srcOffset = self.ebpOffset(src)
        code.append('mov edi, [ebp' + srcOffset + ']')
        code.append('mov esi, [ebp' + dstOffset + ']')
        if flag[0] == 1:
            code.append('mov esi, [esi]')
        if flag[2] == 1:
            code.append('mov edi, [edi]')
        if instr[1] == '+=':
            code.append('add [esi], edi')
        elif instr[1] == '-=':
            code.append('sub [esi], edi')
        elif instr[1] == '*=':
            code.append('imul edi, [esi]')
            code.append('mov [esi], edi')
        elif instr[1] == '/=':
            code.append('xor edx, edx')
            code.append('mov eax, [esi]')
            code.append('idiv edi')
            code.append('mov [esi], eax')
        return code

    def assign_ptr_rhs(self, instr):
        # sz = helper.symbolTables[scopeInfo[1]].get(instr[1])['size']
        # sz = self.get_ident_info(instr[0])['size']
        dst = instr[0]
        src = instr[2]
        flag = self.setFlags(instr)

        offset1 = self.ebpOffset(instr[0])
        offset2 = self.ebpOffset(instr[2])

        self.counter += 1
        label = 'looping' + str(self.counter)
        iters = int(4 / 4)
        code_ = ['mov esi, ebp', 'mov ebx, ebp']
        code_.append('add esi, '+offset1)
        code_.append('add ebx, [ebp' + offset2 + ']')
        if flag[2] == 1:
            code_.append('mov ebx, [ebp' + offset2 + ']')
            code_.append('mov ebx, [ebx]')
        if flag[0] == 1:
            code_.append('mov esi, [ebp' + offset1 + ']')
        code_.append('mov cx, '+str(iters))
        code_.append(label + ':')
        code_.append('mov edx, [ebx]')
        code_.append('mov [esi], edx')
        code_.append('add esi, 4')
        code_.append('add ebx, 4')
        code_.append('dec cx')
        code_.append('jnz '+label)
        return code_

    def add_assign_op(self, instr):
        if instr[0][0] == '*':
            return self.assign_op_ptr(instr)
        # instr.insert(2, instr[1])
        # scopeInfo.insert(2, scopeInfo[1])
        instr1 = []
        instr1.append(instr[0])
        instr1.append("=")
        instr1.append(instr[0])
        if(instr[1] == "+=float"):
            instr1.append("+float")
            instr1.append(instr[2])
            return self.fadd_op(instr1)
        instr1.append("+"+instr[1][2:])
        instr1.append(instr[2])
        return self.add_op(instr1)

    def sub_assign_op(self, instr):
        if instr[0][0] == '*':
            return self.assign_op_ptr(instr)
        # instr.insert(2, instr[1])
        # scopeInfo.insert(2, scopeInfo[1])

        instr1 = []
        instr1.append(instr[0])
        instr1.append("=")
        instr1.append(instr[0])
        if(instr[1] == "-=float"):
            instr1.append("-float")
            instr1.append(instr[2])
            return self.fsub_op(instr1)
        instr1.append("-"+instr[1][2:])
        instr1.append(instr[2])
        return self.sub_op(instr1)

    def mul_assign_op(self, instr):
        if instr[0][0] == '*':
            return self.assign_op_ptr(instr)
        # instr.insert(2, instr[1])
        # scopeInfo.insert(2, scopeInfo[1])
        instr1 = []
        instr1.append(instr[0])
        instr1.append("=")
        instr1.append(instr[0])
        if(instr[1] == "*=float"):
            instr1.append("*float")
            instr1.append(instr[2])
            return self.fmul_op(instr1)
        instr1.append("*"+instr[1][2:])
        instr1.append(instr[2])
        return self.mul_op(instr1)

        # return self.mul_op(instr)

    def div_assign_op(self, instr):
        if instr[0][0] == '*':
            return self.assign_op_ptr(instr)
        # instr.insert(2, instr[1])
        # scopeInfo.insert(2, scopeInfo[1])
        instr1 = []
        instr1.append(instr[0])
        instr1.append("=")
        instr1.append(instr[0])
        if(instr[1] == "/=float"):
            instr1.append("/float")
            instr1.append(instr[2])
            return self.fdiv_op(instr1)
        instr1.append("*"+instr[1][2:])
        instr1.append(instr[2])
        return self.div_op(instr1)

        # return self.div_op(instr)

    def ampersand_op(self, instr):
        dst = instr[0]
        src = instr[3]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        srcOffset = self.ebpOffset(src)
        code = []

        if flag[2] == 1:
            code.append('mov edi, [ebp' + srcOffset + ']')
        else:
            code.append('lea edi, [ebp' + srcOffset + ']')

        if flag[0] == 1:
            code.append('mov esi, [ebp' + dstOffset + ']')
            code.append('mov [esi], edi')
        else:
            code.append('mov [ebp'+dstOffset+'], edi')

        return code

    def relops_cmp(self, instr):
        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        src1Offset = self.ebpOffset(src1)
        src2Offset = self.ebpOffset(src2)
        # print("Instr1", instr[1])
        code = []

        if(src1Offset == -1):
            code.append('mov edi, '+str(src1))
        else:
            code.append('mov edi, [ebp' + str(src1Offset) + ']')
        if flag[2] == 1:
            code.append('mov edi, [edi]')

        if (src2Offset == -1):
            code.append('mov esi, '+str(src2))
        else:
            code.append('mov esi, [ebp' + str(src2Offset) + ']')
        if flag[4] == 1:
            code.append('mov esi, [esi]')
        code.append('xor eax, eax')
        code.append('cmp edi, esi')
        if instr[3] == '==int':
            code.append('sete al')
        elif instr[3] == '!=int':
            code.append('setne al')
        elif instr[3] == '<int':
            code.append('setl al')
        elif instr[3] == '>int':
            code.append('setg al')
        elif instr[3] == '<=int':
            code.append('setle al')
        elif instr[3] == '>=int':
            code.append('setge al')

        if flag[0] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], eax')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], eax')
        return code

    def relops_fcmp(self, instr):
        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        src1Offset = self.ebpOffset(src1)
        src2Offset = self.ebpOffset(src2)

        code = []
        code.append('fld dword [ebp' + str(src1Offset) + ']')
        # if flag[2] == 1:
        #     code.append('mov edi, [edi]')
        code.append('fld dword [ebp' + str(src2Offset) + ']')
        # if flag[3] == 1:
        #     code.append('mov esi, [esi]')
        code.append('xor eax, eax')
        code.append('fcomip')
        # code.append('sahf')
        code.append('fstp dword [temp]')
        # code.append('mov al, c0')
        if instr[3] == '==float':
            code.append('sete al')
        elif instr[3] == '!=float':
            code.append('setne al')
        elif instr[3] == '<float':
            code.append('setl al')
        elif instr[3] == '>float':
            code.append('setg al')
        elif instr[3] == '<=float':
            code.append('setle al')
        elif instr[3] == '>=float':
            code.append('setge al')

        if flag[0] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], eax')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], eax')
        return code

    def print_int(self, instr):
        src = instr[1]
        srcOffset = self.ebpOffset(src)
        flag = self.setFlags(instr)
        code = []
        if(srcOffset == -1):
            code.append('mov esi, ' + src)
        else:
            code.append('mov esi, [ebp' + srcOffset + ']')
        if flag[1] == 1:
            code.append('mov esi, [esi]')
        code.append('push esi')
        code.append('push print_int')
        code.append('call printf')
        code.append('pop esi')
        code.append('pop esi')
        return code

    def print_float(self, instr):
        src = instr[1]
        srcOffset = self.ebpOffset(src)
        # flag = self.setFlags(instr)
        code = []
        if srcOffset != -1:
            code.append('fld dword [ebp' + srcOffset + ']')
        else:
            binaryCode = binary(float(src))
            code.append('mov edi, 0b' + str(binaryCode))
            code.append('mov esi, [ebp-4]')
            code.append('mov [ebp-4], edi')
            code.append('fld dword [ebp-4]')
            code.append('mov [ebp-4], esi')
        code.append('fstp qword [temp]')
        code.append('push dword [temp+4]')
        code.append('push dword [temp+4]')
        code.append('push dword farray_print')
        code.append('call printf')
        code.append('add esp, 12')

        return code

    def print_string(self, instr):
        src = instr[1]
        # flag = self.setFlags(instr)
        srcOffset = self.ebpOffset(src)
        code = []
        code.append('mov esi, [ebp' + srcOffset + ']')
        code.append('push esi')
        code.append('call puts')
        code.append('pop esi')
        return code

    def scan_int(self, instr):
        src = instr[1]
        flag = self.setFlags(instr)
        srcOffset = self.ebpOffset(src)
        code = []
        code.append('lea esi, [ebp' + srcOffset + ']')
        if flag[1] == 1:
            code.append('mov esi, [esi]')
        code.append('push esi')
        code.append('push scan_int')
        code.append('call scanf')
        code.append('pop esi')
        code.append('pop esi')
        return code

    def scan_string(self, instr):
        src = instr[1]
        flag = self.setFlags(instr)
        srcOffset = self.ebpOffset(src)
        code = []

        code.append('mov edi, 100')
        code.append('call malloc')
        code.append('pop edi')
        code.append('mov [ebp' + srcOffset + '],  eax')
        code.append('mov esi, eax')

        code.append('push esi')
        code.append('call gets')
        code.append('pop esi')
        return code

    def param(self, instr):
        # data_ = helper.symbolTables[scopeInfo[1]].get(instr[1])
        data_ = self.get_ident_info(instr[1])
        if data_ == -1:
            return ['push ' + str(instr[1])]
        baseType = data_['type']
        flag = self.setFlags(instr)
        offset = self.ebpOffset(instr[1])
        if baseType[0] in ['int', 'bool', 'float', 'string'] or baseType == 'temp':
            if flag[1] == 1:
                return [
                    'mov edx, [ebp' + offset + ']',
                    'mov edx, [edx]',
                    'push edx',
                ]
            else:
                return ['mov edx, [ebp' + offset + ']', 'push edx']
        else:
            self.counter += 1
            label = 'looping' + str(self.counter)
            iters = int(data_['size'] / 4)
            code_ = ['mov esi, ebp']
            code_.append('add esi, '+offset)
            if flag[1] == 1:
                code_.append('mov esi, [ebp'+offset+']')
            code_.append('add esi, ' + str(data_['size'] - 4))
            code_.append('mov cx, '+str(iters))
            code_.append(label + ':')
            code_.append('mov edx, [esi]')
            code_.append('push edx')
            code_.append('sub esi, 4')
            code_.append('dec cx')
            code_.append('jnz '+label)
            return code_

    def if_op(self, instr):
        var = instr[1]
        jLabel = instr[3]
        code = []
        flag = self.setFlags(instr)

        varOffset = self.ebpOffset(var)
        code.append('mov edi, [ebp' + varOffset + ']')
        if flag[1] == 1:
            code.append('mov edi, [edi]')
        code.append('cmp edi, 0')
        code.append('je ' + jLabel)
        return code

    def goto_op(self, instr):
        jLabel = instr[1]
        code = []

        code.append('jmp ' + jLabel)
        return code

    def logical(self, instr):
        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        src1Offset = self.ebpOffset(src1)
        src2Offset = self.ebpOffset(src2)

        code = []
        if(src1Offset == -1):
            code.append('mov edi, '+str(src1))
        else:
            code.append('mov edi, [ebp' + str(src1Offset) + ']')
        if flag[2] == 1:
            code.append('mov edi, [edi]')

        if (src2Offset == -1):
            code.append('mov esi, '+str(src2))
        else:
            code.append('mov esi, [ebp' + str(src2Offset) + ']')
        if flag[4] == 1:
            code.append('mov esi, [esi]')

        if instr[3] == '||':
            code.append('or edi, esi')
        elif instr[3] == '&&':
            code.append('and edi, esi')

        if flag[0] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], edi')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], edi')
        return code

    def getRetVal(self, instr):
        # data_ = helper.symbolTables[scopeInfo[1]].get(instr[1])
        data_ = self.get_ident_info(instr[1])
        offset = self.ebpOffset(instr[1])

        self.counter += 1
        label = 'looping' + str(self.counter)
        iters = int(data_['size'] / 4)
        code_ = ['mov esi, ebp']
        code_.append('add esi, '+offset)
        code_.append('mov cx, '+str(iters))
        code_.append(label + ':')
        code_.append('mov edx, [eax]')
        code_.append('mov [esi], edx')
        code_.append('add esi, 4')
        code_.append('add eax, 4')
        code_.append('dec cx')
        code_.append('jnz '+label)
        return code_

    # def inc_dec(self, instr):
    #     dst = instr[1]
    #     dstOffset = self.ebpOffset(dst)
    #     flag = self.setFlags(instr)

    #     code = []
    #     code.append('mov esi, [ebp' + dstOffset + ']')
    #     if flag[1] == 1:
    #         code.append('mov esi, [esi]')
    #     if instr[0] == '++':
    #         code.append('inc esi')
    #     else:
    #         code.append('dec esi')

    #     if flag[1] == 1:
    #         code.append('mov edi, [ebp' + str(dstOffset) + ']')
    #         code.append('mov [edi], esi')
    #     else:
    #         code.append('mov [ebp' + str(dstOffset) + '], esi')
    #     return code
    def set_return_val(self, instr):
        data_ = self.get_ident_info(instr[1])
        code_ = []
        if data_ != -1:
            offset = self.ebpOffset(instr[1])
            code_.append('mov eax, [ebp' + str(offset) + ']')
        else:
            code_.append('mov eax, ' + str(instr[1]))
        code_.append('mov esp, ebp')
        code_.append('pop ebp')
        code_.append('ret')
        return code_

    def bit_shift_right(self, instr):
        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            code.append('mov edx, [ebp' + str(src1Offset) + ']')
            if flag[2] == 1:
                code.append('mov edx, [edi]')
        else:
            code.append('mov edx, ' + str(src1))

        if self.get_ident_info(src2) != -1:
            code.append('mov eax, [ebp' + str(src2Offset) + ']')
            if flag[3] == 1:
                code.append('mov eax, [eax]')
        else:
            code.append('mov eax, ' + str(src2))
        code.append('mov ecx, eax')
        code.append('sar edx, cl')

        if flag[1] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], edx')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], edx')
        return code

    def bit_shift_left(self, instr):
        dst = instr[0]
        src1 = instr[2]
        src2 = instr[4]
        flag = self.setFlags(instr)

        dstOffset = self.ebpOffset(dst)
        if self.get_ident_info(src1) != -1:
            src1Offset = self.ebpOffset(src1)
        if self.get_ident_info(src2) != -1:
            src2Offset = self.ebpOffset(src2)

        code = []
        if self.get_ident_info(src1) != -1:
            code.append('mov edx, [ebp' + str(src1Offset) + ']')
            if flag[2] == 1:
                code.append('mov edx, [edx]')
        else:
            code.append('mov edx, ' + str(src1))

        if self.get_ident_info(src2) != -1:
            code.append('mov eax, [ebp' + str(src2Offset) + ']')
            if flag[3] == 1:
                code.append('mov eax, [eax]')
        else:
            code.append('mov eax, ' + str(src2))
        code.append('mov ecx, eax')
        code.append('sal edx, cl')

        if flag[1] == 1:
            code.append('mov esi, [ebp' + str(dstOffset) + ']')
            code.append('mov [esi], edx')
        else:
            code.append('mov [ebp' + str(dstOffset) + '], edx')
        return code

    def genCode(self, idx):
        # Check instruction type and call function accordingly
        instr = self.code[idx]

        if len(instr) == 1 and instr[0] == 'return':
            self.add_epilogue()
            return []
        elif len(instr) == 1 and instr[0] == 'pop':
            return ['pop edi']
        elif len(instr) == 2 and instr[0] == 'return':
            return self.set_return_val(instr)
        elif len(instr) == 2 and instr[1][0] == ':':
            # print("Hello")
            return [instr[0]+':']
        elif len(instr) == 5 and instr[3] == '+int':
            return self.add_op(instr)
        elif len(instr) == 5 and instr[3] == '+float':
            return self.fadd_op(instr)
        elif (len(instr) == 4 and instr[2] == '-float') or (instr[0] == '*' and instr[3] == '-float'):
            return self.unary_fminus(instr)
        elif len(instr) == 5 and instr[3] == '-float':
            return self.fsub_op(instr)

        elif (len(instr) == 4 and instr[2] == '-int') or (instr[0] == '*' and instr[3] == '-int'):
            return self.unary_minus(instr)
        elif len(instr) == 5 and (instr[3] == '-int' or instr[3] == '-arr_int'):
            return self.sub_op(instr)

        # if instr[1] == '-int':
        #     if len(instr) == 4:
        #         return self.sub_op(instr, scopeInfo, funcScope)
        #     else:
        #         return self.unary_minus(instr, scopeInfo, funcScope)
        elif len(instr) == 5 and instr[3] == '*int':
            return self.mul_op(instr)
        elif len(instr) == 5 and instr[3] == '*float':
            return self.fmul_op(instr)
        elif len(instr) == 5 and instr[3] == '/int':
            return self.div_op(instr)
        elif len(instr) == 5 and instr[3] == '/float':
            return self.fdiv_op(instr)
        elif len(instr) == 5 and instr[3] == '<<int':
            return self.bit_shift_left(instr)
        elif len(instr) == 5 and instr[3] == '>>int':
            return self.bit_shift_right(instr)

        elif (len(instr) == 3 and instr[1] == '=') or (len(instr) == 4 and instr[2] == '=') or (len(instr) == 4 and instr[1] == '='):
            return self.assign_op(instr)
        elif len(instr) == 3 and instr[1] == '+=':
            return self.add_assign_op(instr)
        elif len(instr) == 3 and instr[1] == '-=':
            return self.sub_assign_op(instr)
        elif len(instr) == 3 and instr[1] == '*=':
            return self.mul_assign_op(instr)
        elif len(instr) == 3 and instr[1] == '/=':
            return self.div_assign_op(instr)

        elif len(instr) == 5 and instr[0][0:6] == 'retval':
            return self.getRetVal(instr)  # error

        elif len(instr) == 5 and instr[3] in self.relops:
            return self.relops_cmp(instr)

        elif len(instr) == 5 and instr[3] in self.frelops:
            return self.relops_fcmp(instr)

        elif len(instr) == 4 and instr[0] == 'ifnot':
            return self.if_op(instr)
        elif len(instr) == 2 and instr[0] == 'goto':
            return self.goto_op(instr)

        elif len(instr) == 5 and instr[3] in ['||', '&&']:
            return self.logical(instr)

        # elif instr[0] in ['--', '++']:
        #     return self.inc_dec(instr, scopeInfo, funcScope)

        elif instr[0] == 'print_int':
            return self.print_int(instr)
        elif instr[0] == 'print_float':
            return self.print_float(instr)
        elif instr[0] == 'print_string':
            return self.print_string(instr)
        elif instr[0] == 'scan_int':
            return self.scan_int(instr)
        elif instr[0] == 'scan_string':
            return self.scan_string(instr)
        elif len(instr) == 2 and instr[0] == 'param':
            return self.param(instr)
        elif len(instr) == 2 and instr[0] == 'call':
            # function call
            return ['call '+instr[1]]

        elif len(instr) == 5 and instr[0] == '*pointer':
            return self.assign_ptr_rhs(instr)
        elif len(instr) == 4 and instr[2][0] == '&':
            return self.ampersand_op(instr)

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

    codeGen = CodeGen(rootNode, scopetab)

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
