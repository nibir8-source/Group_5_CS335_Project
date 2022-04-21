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
    sub esp, 20
    mov edi, 5
    mov [ebp-4], edi
    mov edi, 6
    mov [ebp-8], edi
    mov edi, [ebp-4]
    mov esi, [ebp-8]
    add edi, esi
    mov [ebp-16], edi
    mov edi, [ebp-16]
    mov [ebp-12], edi
    mov esp, ebp
    pop ebp
    ret
