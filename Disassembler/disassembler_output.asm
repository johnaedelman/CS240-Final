addi $at, $zero, 111
sw $at, 0($gp)
addi $at, $zero, 117
sw $at, 4($gp)
addi $at, $zero, 117
sw $at, 8($gp)
addi $at, $zero, 117
sw $at, 12($gp)
addi $at, $zero, 103
sw $at, 16($gp)
addi $at, $zero, 104
sw $at, 20($gp)
addi $at, $zero, 104
sw $at, 24($gp)
addi $at, $zero, 104
sw $at, 28($gp)
addi $at, $zero, 104
sw $at, 32($gp)
addi $at, $zero, 0
sw $at, 36($gp)
addi $t0, $zero, -4
add $t0, $t0, $gp
addi $t1, $zero, 5
sw $t1, 0($t0)
lw $t1, 0($t0)
addi $t2, $zero, -1
add $t1, $t1, $t2
sw $t1, 0($t0)
addi $t1, $zero, -8
add $t1, $t1, $gp
lw $t2, 0($t0)
sw $t2, 0($t1)
addi $v0, $zero, 1
lw $t2, 0($t0)
add $a0, $t2, $zero
syscall
addi $v0, $zero, 4
addi $a0, $zero, 0
syscall
addi $v0, $zero, 1
lw $t2, 0($t1)
add $a0, $t2, $zero
syscall
