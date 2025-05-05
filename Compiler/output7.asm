main:
addi $t0, $zero, 268468220
addi $t1, $zero, 268468216
addi $t2, $zero, 268468212
addi $t3, $zero, 7
sw $t3, 0($t0)
addi $t3, $zero, 18
sw $t3, 0($t1)
lw $t3, 0($t0)
sw $t3, 0($t2)
addi $t3, $zero, 19
sw $t3, 0($t1)
addi $t3, $zero, 13
sw $t3, 0($t2)
addi $t3, $zero, 268468208
addi $t4, $zero, 1
sw $t4, 0($t3)
loop1:
addi $t4, $zero, 1
sw $t4, 0($t0)
addi $t4, $zero, 2
sw $t4, 0($t1)
endloop1:
lw $t4, 0($t3)
addi $t4, $t4, 1
sw $t4, 0($t3)
ble $t4, 99, loop1
