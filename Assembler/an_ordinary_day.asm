# an ordinary day

roll $t6, 6     # decide what to do for the day
hit $t1, $t4    # attack monster
hit $t1, $t4    # attack monster
hurt $t0, $t3, 10 # takes damage from weak monster
heal $t0, $t3   # drink healing potion
hit $t1, $t4    # attack monster
absorb $t0, $t3, 5 # convert damage to health

