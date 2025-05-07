addi $at, $zero, 10
sw $at, 0($gp)
addi $at, $zero, 0
sw $at, 4($gp)
addi $at, $zero, 66
sw $at, 8($gp)
addi $at, $zero, 117
sw $at, 12($gp)
addi $at, $zero, 122
sw $at, 16($gp)
addi $at, $zero, 122
sw $at, 20($gp)
addi $at, $zero, 10
sw $at, 24($gp)
addi $at, $zero, 0
sw $at, 28($gp)
addi $at, $zero, 70
sw $at, 32($gp)
addi $at, $zero, 105
sw $at, 36($gp)
addi $at, $zero, 122
sw $at, 40($gp)
addi $at, $zero, 122
sw $at, 44($gp)
addi $at, $zero, 10
sw $at, 48($gp)
addi $at, $zero, 0
sw $at, 52($gp)
addi $at, $zero, 70
sw $at, 56($gp)
addi $at, $zero, 105
sw $at, 60($gp)
addi $at, $zero, 122
sw $at, 64($gp)
addi $at, $zero, 122
sw $at, 68($gp)
addi $at, $zero, 66
sw $at, 72($gp)
addi $at, $zero, 117
sw $at, 76($gp)
addi $at, $zero, 122
sw $at, 80($gp)
addi $at, $zero, 122
sw $at, 84($gp)
addi $at, $zero, 10
sw $at, 88($gp)
addi $at, $zero, 0
sw $at, 92($gp)
addi $t0, $zero, -4
add $t0, $t0, $gp
addi $t1, $zero, 1
sw $t1, 0($t0)
label0:
addi $t1, $zero, 5
lw $t2, 0($t0)
div $t2, $t1
mfhi $t1
addi $t2, $zero, 0
bne $t1, $t2, label1
addi $t1, $zero, 3
lw $t2, 0($t0)
div $t2, $t1
mfhi $t1
addi $t2, $zero, 0
bne $t1, $t2, label1
addi $v0, $zero, 4
addi $a0, $zero, 56
syscall
j label4
label1:
addi $t1, $zero, 3
lw $t2, 0($t0)
div $t2, $t1
mfhi $t1
addi $t2, $zero, 0
bne $t1, $t2, label2
addi $v0, $zero, 4
addi $a0, $zero, 32
syscall
j label4
label2:
addi $t1, $zero, 5
lw $t2, 0($t0)
div $t2, $t1
mfhi $t1
addi $t2, $zero, 0
bne $t1, $t2, label3
addi $v0, $zero, 4
addi $a0, $zero, 8
syscall
label3:
addi $v0, $zero, 1
lw $t1, 0($t0)
add $a0, $t1, $zero
syscall
addi $v0, $zero, 4
addi $a0, $zero, 0
syscall
label4:
lw $t1, 0($t0)
addi $t1, $t1, 1
sw $t1, 0($t0)
addi $at, $zero, 99
slt $at, $at, $t1
beq $at, $zero, label0
