.data
string3: .asciiz "\n"
string2: .asciiz "Buzz\n"
string1: .asciiz "Fizz\n"
string0: .asciiz "FizzBuzz\n"
.text
main:
li $t0, -4
add $t0, $t0, $gp
li $t1, 1
sw $t1, 0($t0)
loop0:
li $t1, 5
lw $t2, 0($t0)
div $t2, $t1
mfhi $t1
li $t2, 0
bne $t1, $t2, skip0
li $t1, 3
lw $t2, 0($t0)
div $t2, $t1
mfhi $t1
li $t2, 0
bne $t1, $t2, skip0
li $v0, 4
la $a0, string0
syscall
j endcond0
skip0:
li $t1, 3
lw $t2, 0($t0)
div $t2, $t1
mfhi $t1
li $t2, 0
bne $t1, $t2, skip1
li $v0, 4
la $a0, string1
syscall
j endcond0
skip1:
li $t1, 5
lw $t2, 0($t0)
div $t2, $t1
mfhi $t1
li $t2, 0
bne $t1, $t2, skip2
li $v0, 4
la $a0, string2
syscall
skip2:
li $v0, 1
lw $t1, 0($t0)
move $a0, $t1
syscall
li $v0, 4
la $a0, string3
syscall
endcond0:
endloop0:
lw $t1, 0($t0)
addi $t1, $t1, 1
sw $t1, 0($t0)
ble $t1, 99, loop0
