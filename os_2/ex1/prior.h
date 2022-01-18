#ifndef _PRIOR_H_
#define _PRIOR_H_

#include <unistd.h>

#include <iostream>
#include <vector>
using namespace std;

enum status { kReady, kRunning, kFinished };

struct PCB {
 public:
  status _current_status;
  int _priority;
  int _all_time;
  int _remaining_time;
  PCB() {
    srand(unsigned(time(NULL)));
    _all_time = rand() % 6 + 1;
    _priority = rand() % 10 + 1;
    _remaining_time = _all_time;
    _current_status = kReady;
    sleep(1);
  }

  void show_info() {
    std::cout << "current_status: " << _current_status
              << "| priority: " << _priority
              << "| remaining_time: " << _remaining_time
              << "| all_time: " << _all_time << std::endl;
  }
};

class PriorSchedule {
 public:
  PriorSchedule(int set_capacity) {
    this->_capacity = set_capacity;
    vec = vector<PCB>(_capacity);
  }

  // bubble sort
  void prior_sort() {
    for (int i = 0; i < _capacity; i++) {
      for (int j = 0; j < _capacity - i - 1; j++) {
        if (vec[j]._priority < vec[j + 1]._priority) {
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
      if (vec[i]._priority >= front._priority) {
        vec[i - 1] = vec[i];
      } else if (vec[i]._priority < front._priority) {
        front._current_status = kReady;
        vec[i - 1] = front;
        return;
      }
    }
    front._current_status = kReady;
    vec[vec.size() - 1] = front;
  }

  PCB &get_front() {
    if (!vec.empty()) {
      return vec[0];
    }
  }

  void process_exec() {
    PCB &front = get_front();

    if (front._current_status == kReady) {
      front._current_status = kRunning;
      front._remaining_time -= 1;
      if (front._remaining_time == 0) {
        vec.erase(begin(vec));
        return;
      }
      if (front._priority >= 3) {
        front._priority -= 3;
      } else
        front._priority = 0;
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
  int _capacity;
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