#include <unistd.h>

#include <iostream>
#include <vector>
using namespace std;

enum status { kRunning, kReady, kFinished };

struct PCB {
  int _remaining_time;
  int _all_time;
  status _current_status;
  PCB() {
    srand(unsigned(time(NULL)));
    _all_time = rand() % 6 + 1;
    _remaining_time = _all_time;
    _current_status = kReady;
    sleep(1);
  }
  void show_info() {
    std::cout << "current_status: " << _current_status
              << "| remaining_time: " << _remaining_time
              << "| all_time: " << _all_time << std::endl;
  }
};

class RoundRobin {
 public:
  RoundRobin(int set_capacity) : _capacity(set_capacity) {
    schedule_queue = vector<PCB>(set_capacity);
  }

  void show_all_info() {
    for (int i = 0; i < schedule_queue.size(); i++) {
      schedule_queue[i].show_info();
    }
    std::cout << endl;
  }

  PCB &get_front() {
    if (!schedule_queue.empty()) return schedule_queue[0];
  }

  bool queue_empty() {
    if (schedule_queue.empty()) return true;
    return false;
  }

  void resort() {
    PCB temp = schedule_queue[0];
    int i = 1;
    for (; i < schedule_queue.size(); i++) {
      schedule_queue[i - 1] = schedule_queue[i];
    }
    temp._current_status = kReady;
    schedule_queue[i - 1] = temp;
  }

  void process_exec() {
    PCB &front = get_front();
    if (front._current_status == kReady) front._current_status = kRunning;
    front._remaining_time -= 1;
    if (front._remaining_time == 0) {
      schedule_queue.erase(begin(schedule_queue));
      return;
    }
    resort();
  }

 private:
  vector<PCB> schedule_queue;
  int _capacity;
};

void test_pipeline() {
  RoundRobin test = RoundRobin(5);
  test.show_all_info();
  int count = 0;
  while (!test.queue_empty()) {
    test.process_exec();
    std::cout << count << endl;
    test.show_all_info();
    count++;
  }
}