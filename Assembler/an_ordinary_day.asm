# an ordinary day

li $t6, 0
li $t4, 100
roll $t6, 6     # decide what to do for the day
hit $t1, $t4    # attack monster
move $t4, $t1
hit $t1, $t4    # attack monster
li $t3, 400
hurt $t0, $t3, 96 # takes damage from weak monster
move $t3, $t0
heal $t0, $t3   # drink healing potion
move $t4, $t1
hit $t1, $t4    # attack monster
li $t3, 100
absorb $t0, $t3, 5 # convert damage to health

