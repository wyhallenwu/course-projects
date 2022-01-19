#include <deque>
#include <iostream>
#include <vector>
using namespace std;

struct Process {
  vector<int> _need;
  vector<int> _max;

  Process(vector<int> need, vector<int> max) {
    _need = need;
    _max = max;
  }

  friend ostream& operator<<(ostream& out, const Process& process) {
    out << "Need: " << '[';
    for (int i = 0; i < process._need.size(); i++) {
      out << process._need[i] << ',';
    }

    out << ']' << endl << "Max: " << '[';
    for (int i = 0; i < process._max.size(); i++) {
      out << process._max[i] << ',';
    }
    out << ']' << endl;
  }
};

class BankersAlgorithm {
 private:
  vector<int> _available;
  vector<int> _allocation;
  vector<Process> _process_list;

 public:
  BankersAlgorithm(vector<int> available, vector<int> allocation) {
    _available = available;
    _allocation = allocation;
    _process_list.clear();
  }

  friend ostream& operator<<(ostream& out, const BankersAlgorithm& ba) {
    out << "Available: "
        << "[";
    for (int i = 0; i < ba._available.size(); i++) {
      out << ba._available[i] << ",";
    }
    out << "]" << endl
        << "Allocation: "
        << "[";
    for (int i = 0; i < ba._allocation.size(); i++) {
      out << ba._allocation[i] << ",";
    }
    out << "]" << endl;

    for (int i = 0; i < ba._process_list.size(); i++) {
      out << "process: " << i << endl << ba._process_list[i];
    }
  }

  void process_coming(Process process) { _process_list.push_back(process); }

  bool examine_basic(const vector<int>& consume, const Process& process) {
    for (int i = 0; i < consume.size(); i++) {
      if (consume[i] > _available[i] || consume[i] > process._need[i])
        return false;
    }
    return true;
  }

  bool isFinished(const deque<bool>& finished) {
    for (int i = 0; i < finished.size(); i++) {
      if (finished[i] == false) return false;
    }
    return true;
  }

  void compute(vector<int>& avail, const vector<int> consume) {
    for (int i = 0; i < avail.size(); i++) {
      avail[i] += consume[i];
    }
  }

  void refine(vector<int> request) {
    for (int i = 0; i < _available.size(); i++) {
      _available[i] -= request[i];
    }
  }

  bool isMeet(Process& process) {
    for (int i = 0; i < process._need.size(); i++) {
      if (process._need[i] > _available[i]) return false;
    }
    return true;
  }

  bool examine(vector<int> consume, int index) {
    if (!examine_basic(consume, _process_list[index])) return false;
    deque<bool> finished(_process_list.size(), false);
    finished[index] = true;
    for (int i = 0; i < _process_list.size(); i++) {
      _available[i] -= _process_list[index]._need[i];
    }
    vector<int> available_temp = _available;
    return ba_help(finished, available_temp);
  }

  bool ba_help(deque<bool>& finished, vector<int>& available_temp) {
    if (isFinished(finished)) return true;
    for (int i = 0; i < _process_list.size() && finished[i] == false; i++) {
      if (isMeet(_process_list[i])) {
        vector<int> request = _process_list[i]._need;
        compute(available_temp, _process_list[i]._need);
        finished[i] == true;
        if (!ba_help(finished, available_temp)) {
          refine(request);
          return false;
        } else
          return true;
      }
    }
    if (isFinished(finished))
      return true;
    else
      return false;
  }

  void pipeline(vector<int> consume, int index) {
    if (examine(consume, index))
      cout << "safe" << endl;
    else
      cout << "not safe" << endl;
  }
};