
#include <stdio.h>

int main(){
    int bosses_beaten = 0;
    for (int hours_played = 1; hours_played <= 140; hours_played++){
        printf("Hours played: %d\n", hours_played)
        if (hours_played % 8 == 0){
            bosses_beaten = bosses_beaten + 1
            printf("You beat a boss! You've beaten %d bosses.\n", bosses_beaten);
            if (bosses_beaten == 17){
            printf("Congratulations! You beat the final boss! Get this man a Mythical Last Prism.\n")
            }
        }
    }
}