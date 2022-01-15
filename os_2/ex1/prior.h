#ifndef _PRIOR_H_
#define _PRIOR_H_

#include <iostream>
#include <vector>

enum status {kReady, kRunning, kFinished};
struct PCB {
    status current_status;
    int priority;
    int all_time;
    int remaining_time;
    int exec_count;

    PCB() {
        all_time = rand() % 6 + 1;
        priority = rand() % 10 + 1;
        remaining_time = all_time;
        current_status = kReady;
        exec_count = 0;
    }

    void show_info() {
        std::cout << "current_status: " << current_status
            << "| priority: " << priority
            << "| remaining_time: " << remaining_time
            << "| exec_count: " << exec_count
            << "| all_time: " << all_time << std::endl;
    }

};



#endif