global main
extern printf
extern scanf
extern gets
extern puts
extern farray_print
extern malloc
section .data
    temp dq 0
    print_int db "%i ", 0x00
    farray_print db "%f ", 0x0a, 0x00
    print_line db "", 0x0a, 0x00
    scan_int db "%d", 0
section .text
main:
    push ebp
    mov ebp, esp
    sub esp, 36
    mov edi, 2
    mov [ebp-8], edi
    lea esi, [ebp-4]
    push esi
    push scan_int
    call scanf
    pop esi
    pop esi
    mov edi, [ebp-8]
    mov esi, 1
    xor eax, eax
    cmp edi, esi
    sete al
    mov [ebp-12], eax
    mov edi, [ebp-12]
    cmp edi, 0
    je label_no_3
    mov esi, 1
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    jmp label_no_2
label_no_3:
    mov edi, [ebp-8]
    mov esi, 2
    xor eax, eax
    cmp edi, esi
    sete al
    mov [ebp-16], eax
    mov edi, [ebp-16]
    cmp edi, 0
    je label_no_4
    mov esi, 2
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    jmp label_no_2
label_no_4:
    mov edi, [ebp-8]
    mov esi, 1
    add edi, esi
    mov [ebp-20], edi
    mov edi, [ebp-8]
    mov esi, [ebp-20]
    xor eax, eax
    cmp edi, esi
    sete al
    mov [ebp-28], eax
    mov edi, [ebp-28]
    cmp edi, 0
    je label_no_5
    mov edi, [ebp-8]
    mov esi, 1
    add edi, esi
    mov [ebp-24], edi
    mov esi, [ebp-24]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    jmp label_no_2
label_no_5:
    mov edi, [ebp-8]
    mov esi, 4
    xor eax, eax
    cmp edi, esi
    sete al
    mov [ebp-32], eax
    mov edi, [ebp-32]
    cmp edi, 0
    je label_no_6
    mov esi, 4
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    jmp label_no_2
label_no_6:
    mov esi, 100
    push esi
    push print_int
    call printf
    pop esi
    pop esi
label_no_2:
    mov esp, ebp
    pop ebp
    ret
