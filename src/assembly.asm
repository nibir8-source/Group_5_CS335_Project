global main
extern printf
extern scanf
extern malloc
section .data
    temp dq 0
    print_int db "%i ", 0x00
    farray_print db "%f ", 0x0a, 0x00
    print_line db "", 0x0a, 0x00
    scan_int db "%d", 0
section .text
fact:
    push ebp
    mov ebp, esp
    sub esp, 20
    mov edi, [ebp+8]
    mov esi, 1
    xor eax, eax
    cmp edi, esi
    sete al
    mov [ebp-4], eax
    mov edi, [ebp-4]
    cmp edi, 0
    je label_no_0
    mov eax, [ebp+8]
    jmp label_no_1
label_no_0:
    mov edi, [ebp+8]
    mov esi, 1
    sub edi, esi
    mov [ebp-8], edi
    mov edx, [ebp-8]
    push edx
    call fact
    mov edi, eax
    mov [ebp-12], edi
    mov edi, [ebp+8]
    mov esi, [ebp-12]
    imul edi, esi
    mov [ebp-16], edi
    mov eax, [ebp-16]
label_no_1:
    mov esp, ebp
    pop ebp
    ret
main:
    push ebp
    mov ebp, esp
    sub esp, 12
    push 7
    call fact
    mov edi, eax
    mov [ebp-4], edi
    mov edi, [ebp-4]
    mov [ebp-8], edi
    mov esi, [ebp-8]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esp, ebp
    pop ebp
    ret
