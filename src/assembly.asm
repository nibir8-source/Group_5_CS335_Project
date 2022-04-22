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
    sub esp, 12
    mov edi, 10
    mov [ebp-4], edi
    mov edi, 10
    mov [ebp-8], edi
    mov esi, [ebp-4]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esi, [ebp-8]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esi, 111
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esp, ebp
    pop ebp
    ret
