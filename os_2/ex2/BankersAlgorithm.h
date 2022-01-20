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

  void refine(vector<int>& availabel_temp, const vector<int>& request) {
    for (int i = 0; i < availabel_temp.size(); i++) {
      availabel_temp[i] -= request[i];
    }
  }

  bool isMeet(const vector<int>& need, const vector<int>& available) {
    for (int i = 0; i < need.size(); i++) {
      if (need[i] > available[i]) return false;
    }
    return true;
  }

  bool examine(vector<int> consume, int index) {
    if (!examine_basic(consume, _process_list[index])) return false;
    deque<bool> finished(_process_list.size(), false);
    finished[index] = true;
    for (int i = 0; i < _available.size(); i++) {
      _available[i] -= consume[i];
    }
    vector<int> available_temp = _available;
    bool flag = false;
    //
    for (int i = 0; i < available_temp.size(); i++)
      cout << available_temp[i] << " ";
    cout << endl;
    //
    ba_help(finished, available_temp, index, flag);

    return flag;
  }

  void ba_help(deque<bool>& finished, vector<int>& available_temp, int current,
               bool& flag) {
    if (isFinished(finished)) {
      flag = true;
      return;
    }
    for (int i = 0; i < _process_list.size() && finished[i] == false; i++) {
      if (isMeet(_process_list[i]._need, available_temp)) {
        compute(available_temp, _process_list[i]._need);
        finished[i] = true;
        //
        for (int j = 0; j < available_temp.size(); j++)
          cout << available_temp[j] << " ";
        cout << endl;
        //
        ba_help(finished, available_temp, i, flag);
      }
    }
    refine(available_temp, _process_list[current]._need);
  }

  void pipeline(vector<int> consume, int index) {
    if (examine(consume, index))
      cout << "safe" << endl;
    else
      cout << "not safe" << endl;
  }
};