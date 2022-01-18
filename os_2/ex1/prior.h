#ifndef _PRIOR_H_
#define _PRIOR_H_

#include <unistd.h>

#include <iostream>
#include <vector>
using namespace std;

enum status { kReady, kRunning, kFinished };

struct PCB {
 public:
  status current_status;
  int priority;
  int all_time;
  int remaining_time;
  PCB() {
    srand(unsigned(time(NULL)));
    all_time = rand() % 6 + 1;
    priority = rand() % 10 + 1;
    remaining_time = all_time;
    current_status = kReady;
    sleep(1);
  }

  void show_info() {
    std::cout << "current_status: " << current_status
              << "| priority: " << priority
              << "| remaining_time: " << remaining_time
              << "| all_time: " << all_time << std::endl;
  }
};

class PriorSchedule {
 public:
  PriorSchedule(int set_capacity) {
    this->capacity = set_capacity;
    vec = vector<PCB>(capacity);
  }

  // bubble sort
  void prior_sort() {
    for (int i = 0; i < capacity; i++) {
      for (int j = 0; j < capacity - i - 1; j++) {
        if (vec[j].priority < vec[j + 1].priority) {
          PCB temp = vec[j];
          vec[j] = vec[j + 1];
          vec[j + 1] = temp;
        }
      }
    }
  }

  void resort(PCB front) {
    int i = 1;
    for (; i < vec.size(); i++) {
      if (vec[i].priority >= front.priority) {
        vec[i - 1] = vec[i];
      } else if (vec[i].priority < front.priority) {
        front.current_status = kReady;
        vec[i - 1] = front;
        return;
      }
    }
    front.current_status = kReady;
    vec[vec.size() - 1] = front;
  }

  PCB &get_front() {
    if (!vec.empty()) {
      return vec[0];
    }
  }

  void process_exec() {
    PCB &front = get_front();

    if (front.current_status == kReady) {
      front.current_status = kRunning;
      front.remaining_time -= 1;
      if (front.remaining_time == 0) {
        vec.erase(begin(vec));
        return;
      }
      if (front.priority >= 3) {
        front.priority -= 3;
      } else
        front.priority = 0;
      resort(front);
    }
  }

  void show_queue() {
    for (int i = 0; i < vec.size(); i++) {
      vec[i].show_info();
    }
    cout << endl;
  }

  bool queue_empty() {
    if (vec.empty()) {
      return true;
    }
    return false;
  }

 private:
  vector<PCB> vec;
  int capacity;
};

void test_pipeline() {
  PriorSchedule test = PriorSchedule(5);
  test.show_queue();
  test.prior_sort();
  test.show_queue();
  int count = 0;
  while (!test.queue_empty()) {
    cout << "current round: " << count << endl;
    test.process_exec();
    test.show_queue();
    count++;
  }
}

#endif