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
    sub esp, 104
    mov edi, "Hello"
    mov [ebp-4], edi
    mov edi, 100
    call malloc
    pop edi
    mov [ebp-4],  eax
    mov esi, eax
    push esi
    call gets
    pop esi
    mov esi, [ebp-4]
    push esi
    call puts
    pop esi
    mov esp, ebp
    pop ebp
    ret
