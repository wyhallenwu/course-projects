#ifndef _PRIOR_H_
#define _PRIOR_H_

#include <iostream>
#include <vector>
// #include<stdlib.h>

enum status {kReady, kRunning, kFinished};
struct PCB {
    status current_status;
    int priority;
    int all_time;
    int remaining_time;
    int exec_count;

    PCB() : current_status(kReady), exec_count(0) {
        unsigned seed = time(0);
        srand(seed);
        all_time = rand() % 6 + 1;
        priority = rand() % 4 + 1;
        remaining_time = all_time;
    }

    void show_info() {
        std::cout << "current_status: " << current_status
            << "| remaining_time: " << remaining_time
            << "| exec_count: " << exec_count
            << "| all_time: " << all_time << std::endl;
    }
};


#endif