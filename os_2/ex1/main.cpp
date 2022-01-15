#include <iostream>
#include <queue>
#include <vector>
#include "prior.h"
using namespace std;

class PriorSchedule {
private:
    vector<PCB> vec;
    int capacity;
public:
    PriorSchedule(int set_capacity) {
        this->capacity = set_capacity;
        vec = vector<PCB>(capacity);
        int count = 0;
        while(count < capacity) {
            PCB *to_insert = new PCB;
            vec[count] = *to_insert;
        }
    }
    
    // bubble sort
    void prior_sort() {
        for(int i = 0; i < capacity; i++) {
            for(int j = 0; j < capacity; - i - 1; j++) {
                if(vec[j].priority < vec[j + 1].priority) {
                    PCB temp = vec[j];
                    vec[j] = vec[j + 1];
                    vec[j + 1] = temp;
                }
            }
        }
    }

    PCB get_front() {
        if(vec.empty())
            return ;
        PCB temp = vec[0];
        return temp;
    }

    void process_exec() {
        PCB front = get_front();
        front.current_status = kRunning;
        

    }
    

}

int main(){

}