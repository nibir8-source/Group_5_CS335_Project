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
main:
    push ebp
    mov ebp, esp
    sub esp, 40
    mov edi, 10
    mov [ebp-4], edi
    mov edi, 15
    mov [ebp-8], edi
    mov edi, [ebp-4]
    mov esi, [ebp-8]
    add edi, esi
    mov [ebp-12], edi
    mov edi, [ebp-12]
    mov [ebp-16], edi
    mov edi, 5
    mov edi, 3
    xor eax, eax
    cmp edi, esi
    setg al
    mov [ebp-20], eax
    mov edi, [ebp-20]
    cmp edi, 0
    je label_no_0
    mov edi, 10
    mov [ebp-24], edi
    mov edi, 19
    mov [ebp-28], edi
    mov edi, [ebp-24]
    mov esi, [ebp-28]
    add edi, esi
    mov [ebp-32], edi
    mov edi, [ebp-32]
    mov [ebp-36], edi
label_no_0:
    mov esp, ebp
    pop ebp
    ret
