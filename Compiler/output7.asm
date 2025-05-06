.data
string0: .asciiz " ouuughhhh "
.text
main:
li $t0, 268468220
li $t1, 5
sw $t1, 0($t0)
lw $t1, 0($t0)
li $t2, -1
add $t1, $t1, $t2
sw $t1, 0($t0)
li $t1, 268468216
lw $t2, 0($t0)
sw $t2, 0($t1)
li $v0, 1
lw $t2, 0($t0)
move $a0, $t2
syscall
li $v0, 4
la $a0, string0
syscall
li $v0, 1
lw $t2, 0($t1)
move $a0, $t2
syscall
