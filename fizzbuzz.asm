.data
str1: .asciiz "Fizz"
str2: .asciiz "Buzz"
.text
li $t0, 1
li $t1, 3
li $t2, 5

LOOP:
div $t0, $t1
mfhi $t3
beq $t3, $zero, FIZZ
div $t0, $t2
mfhi $t3
beq $t3, $zero, BUZZ
li $v0, 1
move $a0, $t0
syscall
addi $t0, $t0, 1
li $v0, 11
li $a0, 10
syscall
ble $t0, 99, LOOP
li $v0, 10
syscall

FIZZ:
li $v0, 4
la $a0, str1
syscall
div $t0, $t2
mfhi $t3
beq $t3, $zero, BUZZ
li $v0, 11
li $a0, 10
syscall
addi $t0, $t0, 1
ble $t0, 100, LOOP
li $v0, 10
syscall

BUZZ:
li $v0, 4
la $a0, str2
syscall
li $v0, 11
li $a0, 10
syscall
addi $t0, $t0, 1
ble $t0, 100, LOOP
li $v0, 10
syscall