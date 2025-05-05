// FizzBuzz in C
#include <stdio.h>

int main() {  // 1
    for (int i = 1; i <= 100; i++){  // 2
        if (i % 5 == 0 && i % 3 == 0){  // 3
            printf("FizzBuzz\n");  // 4
        } else if (i % 3 == 0){  // 5
            printf("Fizz\n");  // 6
        } else if (i % 5 == 0){  // 7
            printf("Buzz\n");  // 8
        } else{  // 9
            printf("%d\n", i);  // 10
        }
    }
    return 0;  // 11
}