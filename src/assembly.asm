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
    sub esp, 16
    mov edi, 23
    mov [ebp-0], edi
    mov edi, 45
    mov [ebp-4], edi
    mov edi, [ebp-0]
    mov esi, [ebp-4]
    add edi, esi
    mov [ebp-4], edi
    mov edx, [ebp-0]
    mov eax, 2
    mov ecx, eax
    sal edx, cl
    mov [ebp-8], edx
    mov edx, [ebp-4]
    mov eax, 2
    mov ecx, eax
    sar edx, cl
    mov [ebp-12], edx
    mov esi, [ebp-0]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esi, [ebp-4]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
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
    mov esi, [ebp-12]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esp, ebp
    pop ebp
    ret
