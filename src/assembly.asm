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
    sub esp, 144
    mov edi, 0
    mov [ebp-84], edi
label_no_0:
label_no_2:
    mov edi, [ebp-84]
    mov esi, 10
    xor eax, eax
    cmp edi, esi
    setl al
    mov [ebp-88], eax
    mov edi, [ebp-88]
    cmp edi, 0
    je label_no_3
    mov edi, [ebp-84]
    mov [ebp-92], edi
    mov edi, [ebp-92]
    mov esi, 8
    imul edi, esi
    mov [ebp-92], edi
    lea edi, [ebp-4]
    mov esi, [ebp-92]
    sub edi, esi
    mov [ebp-92], edi
    mov edi, [ebp-92]
    mov esi, 0
    add edi, esi
    mov [ebp-96], edi
    mov edi, [ebp-84]
    mov esi, 10
    add edi, esi
    mov [ebp-100], edi
    mov edi, [ebp-100]
    mov esi, [ebp-96]
    mov [esi], edi
    mov edi, [ebp-84]
    mov [ebp-104], edi
    mov edi, [ebp-104]
    mov esi, 8
    imul edi, esi
    mov [ebp-104], edi
    lea edi, [ebp-4]
    mov esi, [ebp-104]
    sub edi, esi
    mov [ebp-104], edi
    mov edi, [ebp-104]
    mov esi, 4
    add edi, esi
    mov [ebp-108], edi
    mov edi, 30
    mov esi, [ebp-108]
    mov [esi], edi
    mov edi, [ebp-84]
    mov [ebp-112], edi
    mov edi, [ebp-112]
    mov esi, 8
    imul edi, esi
    mov [ebp-112], edi
    lea edi, [ebp-4]
    mov esi, [ebp-112]
    sub edi, esi
    mov [ebp-112], edi
    mov edi, [ebp-112]
    mov esi, 0
    add edi, esi
    mov [ebp-116], edi
    mov edi, [ebp-84]
    mov [ebp-120], edi
    mov edi, [ebp-120]
    mov esi, 8
    imul edi, esi
    mov [ebp-120], edi
    lea edi, [ebp-4]
    mov esi, [ebp-120]
    sub edi, esi
    mov [ebp-120], edi
    mov edi, [ebp-120]
    mov esi, 4
    add edi, esi
    mov [ebp-124], edi
    mov edi, [ebp-116]
    mov edi, [edi]
    mov [ebp-128], edi
    mov edi, [ebp-124]
    mov edi, [edi]
    mov [ebp-132], edi
    mov edi, [ebp-128]
    mov esi, [ebp-132]
    add edi, esi
    mov [ebp-136], edi
    mov edi, [ebp-136]
    mov [ebp-140], edi
    mov esi, [ebp-140]
    push esi
    push print_int
    call printf
    pop esi
    pop esi
    mov edi, [ebp-84]
    mov esi, 1
    add edi, esi
    mov [ebp-84], edi
    jmp label_no_2
label_no_3:
label_no_1:
    mov esp, ebp
    pop ebp
    ret
