global main
section .data
section .text
main:
    push ebp
    mov ebp, esp
    sub esp, 16
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
