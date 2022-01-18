#include <unistd.h>

#include <iostream>
#include <vector>
using namespace std;

enum status { kRunning, kReady, kFinished };

struct PCB {
  int remaining_time;
  int all_time;
  status current_status;
  PCB() {
    srand(unsigned(time(NULL)));
    all_time = rand() % 6 + 1;
    remaining_time = all_time;
    current_status = kReady;
    sleep(1);
  }
  void show_info() {
    std::cout << "current_status: " << current_status
              << "| remaining_time: " << remaining_time
              << "| all_time: " << all_time << std::endl;
  }
};

class RoundRobin {
 public:
  RoundRobin(int set_capacity) : capacity(set_capacity) {
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
    temp.current_status = kReady;
    schedule_queue[i - 1] = temp;
  }

  void process_exec() {
    PCB &front = get_front();
    if (front.current_status == kReady) front.current_status = kRunning;
    front.remaining_time -= 1;
    if (front.remaining_time == 0) {
      schedule_queue.erase(begin(schedule_queue));
      return;
    }
    resort();
  }

 private:
  vector<PCB> schedule_queue;
  int capacity;
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