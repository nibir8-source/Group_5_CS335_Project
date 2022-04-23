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
    sub esp, 72
    mov edi, 0
    mov [ebp-20], edi
    mov edi, [ebp-20]
    mov esi, 4
    imul edi, esi
    mov [ebp-20], edi
    lea edi, [ebp-4]
    mov esi, [ebp-20]
    sub edi, esi
    mov [ebp-20], edi
    mov edi, 1
    mov esi, [ebp-20]
    mov [esi], edi
    mov edi, 1
    mov [ebp-24], edi
    mov edi, [ebp-24]
    mov esi, 4
    imul edi, esi
    mov [ebp-24], edi
    lea edi, [ebp-4]
    mov esi, [ebp-24]
    sub edi, esi
    mov [ebp-24], edi
    mov edi, 2
    mov esi, [ebp-24]
    mov [esi], edi
    mov edi, 2
    mov [ebp-28], edi
    mov edi, [ebp-28]
    mov esi, 4
    imul edi, esi
    mov [ebp-28], edi
    lea edi, [ebp-4]
    mov esi, [ebp-28]
    sub edi, esi
    mov [ebp-28], edi
    mov edi, 3
    mov esi, [ebp-28]
    mov [esi], edi
    mov edi, 3
    mov [ebp-32], edi
    mov edi, [ebp-32]
    mov esi, 4
    imul edi, esi
    mov [ebp-32], edi
    lea edi, [ebp-4]
    mov esi, [ebp-32]
    sub edi, esi
    mov [ebp-32], edi
    mov edi, 4
    mov esi, [ebp-32]
    mov [esi], edi
    mov edi, 0
    mov [ebp-36], edi
label_no_0:
label_no_2:
    mov edi, [ebp-36]
    mov esi, 3
    xor eax, eax
    cmp edi, esi
    setl al
    mov [ebp-40], eax
    mov edi, [ebp-40]
    cmp edi, 0
    je label_no_3
    mov edi, [ebp-36]
    mov [ebp-44], edi
    mov edi, [ebp-44]
    mov esi, 4
    imul edi, esi
    mov [ebp-44], edi
    lea edi, [ebp-4]
    mov esi, [ebp-44]
    sub edi, esi
    mov [ebp-44], edi
    mov edi, [ebp-36]
    mov esi, 1
    add edi, esi
    mov [ebp-48], edi
    mov edi, [ebp-48]
    mov [ebp-52], edi
    mov edi, [ebp-52]
    mov esi, 4
    imul edi, esi
    mov [ebp-52], edi
    lea edi, [ebp-4]
    mov esi, [ebp-52]
    sub edi, esi
    mov [ebp-52], edi
    mov edi, [ebp-44]
    mov edi, [edi]
    mov [ebp-56], edi
    mov edi, [ebp-52]
    mov edi, [edi]
    mov [ebp-60], edi
    mov edi, [ebp-56]
    mov esi, [ebp-60]
    add edi, esi
    mov [ebp-64], edi
    mov edi, [ebp-64]
    mov [ebp-68], edi
    mov esi, [ebp-68]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov edi, [ebp-36]
    mov esi, 1
    add edi, esi
    mov [ebp-36], edi
    jmp label_no_2
label_no_3:
label_no_1:
    mov esp, ebp
    pop ebp
    ret
