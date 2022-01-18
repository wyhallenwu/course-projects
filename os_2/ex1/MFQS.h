/**
 * @file MFQS.h
 * @author Yuheng WU
 * @brief
 * @version 0.1
 * @date 2022-01-18
 *suppose we have three queues. The time clips are 1, 2, 4.
 * @copyright Copyright (c) 2022
 *
 */
#include <unistd.h>

#include <iostream>
#include <vector>
using namespace std;

enum status { kReady, kRunning, kFinished };
enum level { kQ1, kQ2, kQ3 };
const int kTimeClip1 = 1;
const int kTimeClip2 = 2;
const int kTimeClip3 = 4;

struct PCB {
  level _current_level;
  status _current_status;
  int _all_time;
  int _remaining_time;

  PCB() : _current_level(kQ1), _current_status(kReady) {
    srand(time(NULL));
    _all_time = rand() % 10 + 1;
    _remaining_time = _all_time;
    sleep(1);
  }

  void show_info() {
    std::cout << "current_status: " << _current_status
              << "| remaining_time: " << _remaining_time
              << "| all_time: " << _all_time
              << "| current_level: " << _current_level << endl;
  }
};

class FirstTwoLevel {
 private:
  vector<PCB> schedule_queue;
  int _capacity;
  int _layer_number;  // 0 represent layer1, 1 represent layer2

 public:
  FirstTwoLevel(int set_capacity = 5, int layer_number = 0)
      : _capacity(set_capacity), _layer_number(layer_number) {
    schedule_queue = vector<PCB>(set_capacity);
    if (_layer_number == 1) schedule_queue.clear();
  }

  void show_fifo_level() {
    if (_layer_number == kQ1)
      cout << "Level 1: " << endl;
    else if (_layer_number == kQ2)
      cout << "Level 2: " << endl;
    for (int i = 0; i < schedule_queue.size(); i++) {
      schedule_queue[i].show_info();
    }
    cout << endl;
  }

  void running(PCB &pcb) {
    if (pcb._current_status == kReady) {
      pcb._current_status = kRunning;
      if (_layer_number == kQ1)
        pcb._remaining_time -= kTimeClip1;
      else if (pcb._current_level == kQ2)
        pcb._remaining_time -= kTimeClip2;
      if (pcb._remaining_time <= 0)
        pcb._current_status = kFinished;
      else
        pcb._current_status = kReady;
    }
  }

  PCB process() {
    if (!schedule_queue.empty()) {
      PCB temp = schedule_queue[0];
      running(temp);
      schedule_queue.erase(begin(schedule_queue));
      return temp;
    }
  }

  void lineup(PCB &pcb) {
    if (pcb._remaining_time > 0) {
      int current_size = schedule_queue.size();
      if (pcb._current_level == kQ1) pcb._current_level = kQ2;
      if (current_size < _capacity && current_size >= 0)
        schedule_queue.push_back(pcb);
    }
  }

  bool level_empty() {
    if (schedule_queue.empty()) return true;
    return false;
  }
};

class ThirdLevel {
 private:
  vector<PCB> schedule_queue;
  int _capacity;
  int _level_number = 3;

 public:
  ThirdLevel(int set_capacity = 5) : _capacity(set_capacity) {
    schedule_queue = vector<PCB>(_capacity);
    schedule_queue.clear();
  }

  void show_third_level() {
    cout << "ThirdLevel: " << endl;
    for (int i = 0; i < schedule_queue.size(); i++) {
      schedule_queue[i].show_info();
    }
    cout << endl;
  }

  void running(PCB &pcb) {
    if (!schedule_queue.empty()) {
      pcb._current_status = kRunning;
      pcb._remaining_time -= kTimeClip3;
    }
  }

  void process() {
    if (!schedule_queue.empty()) {
      PCB temp = schedule_queue[0];
      running(temp);
      if (temp._remaining_time < 0) {
        schedule_queue.erase(begin(schedule_queue));
        return;
      }
      schedule_queue.erase(begin(schedule_queue));
      temp._current_status = kReady;
      schedule_queue.push_back(temp);
    }
  }

  bool level_empty() {
    if (schedule_queue.empty()) return true;
    return false;
  }

  void lineup(PCB temp) {
    if (temp._remaining_time > 0) {
      int current_size = schedule_queue.size();
      temp._current_level = kQ3;
      if (current_size < _capacity && current_size >= 0)
        schedule_queue.push_back(temp);
    }
  }
};

class MFQS {
 private:
  FirstTwoLevel Q1;
  FirstTwoLevel Q2;
  ThirdLevel Q3;
  int _capacity;

 public:
  MFQS(int set_capacity) : _capacity(set_capacity) {
    Q1 = FirstTwoLevel(_capacity, 0);
    Q2 = FirstTwoLevel(_capacity, 1);
    Q3 = ThirdLevel(_capacity);
  }

  void show_all_level() {
    Q1.show_fifo_level();
    Q2.show_fifo_level();
    Q3.show_third_level();
  }

  void process() {
    while (!Q1.level_empty()) {
      PCB temp = Q1.process();
      Q2.lineup(temp);
    }
    show_all_level();
    while (!Q2.level_empty()) {
      PCB temp = Q2.process();
      Q3.lineup(temp);
    }
    show_all_level();
    while (!Q3.level_empty()) {
      Q3.process();
    }
  }
};

void test_pipeline() {
  MFQS test = MFQS(5);
  test.show_all_level();
  test.process();
  test.show_all_level();
}