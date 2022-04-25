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
    sub esp, 32
    mov edi, 10
    mov esi, [ebp-4]
    mov [esi], edi
    mov edi, 20
    mov esi, [ebp-8]
    mov [esi], edi
    mov edi, [ebp-4]
    mov edi, [edi]
    mov [ebp-12], edi
    mov edi, [ebp-8]
    mov edi, [edi]
    mov [ebp-16], edi
    mov esi, [ebp-12]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esi, [ebp-16]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov edi, [ebp-8]
    mov edi, [edi]
    mov [ebp-20], edi
    mov edi, [ebp-20]
    mov esi, [ebp-4]
    mov [esi], edi
    mov edi, [ebp-4]
    mov edi, [edi]
    mov [ebp-24], edi
    mov edi, [ebp-24]
    mov [ebp-12], edi
    mov edi, [ebp-8]
    mov edi, [edi]
    mov [ebp-28], edi
    mov edi, [ebp-28]
    mov [ebp-16], edi
    mov esi, [ebp-12]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esi, [ebp-16]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov esp, ebp
    pop ebp
    ret
