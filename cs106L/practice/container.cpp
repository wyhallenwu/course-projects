#include <deque>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <utility>
#include <vector>

using std::cin;
using std::cout;
using std::endl;

int main() {
  std::vector<int> vec1{1, 2, 3, 5, 4};
  vec1.push_back(6);
  vec1.push_back(2);
  for (auto &iter : vec1) {
    cout << iter << endl;
  }

  std::set<int> s{1, 3, 4, 6, 3};
  cout << "below is set" << endl;
  for (auto iter = s.begin(); iter != s.end(); ++iter) {
    cout << *iter << endl;
  }

  std::map<std::string, int> m;
  m.insert(std::make_pair("china", 1));
  m.insert(std::make_pair("usa", 2));
  for (auto iter = m.begin(); iter != m.end(); ++iter) {
    cout << (*iter).first << " " << (*iter).second << endl;
  }

  std::deque<std::string> de;
  de.push_back("wuyuheng");
  de.push_front("yuhengwu");
  for (auto iter = de.begin(); iter != de.end(); ++iter) {
    cout << *iter;
  }
  cout << endl;
  // using reference when using for-each loop
  for (auto &iter : de) {
    cout << iter;
  }
  cout << endl;

  cout << "testing vector iter and &iter" << endl;
  for (auto iter = vec1.begin(); iter != vec1.end(); ++iter) {
    cout << *iter << endl;
  }
  for (auto iter = vec1.begin(); iter != vec1.end(); ++iter) {
    cout << &iter << endl;
  }
  for (auto &iter : vec1) {
    cout << iter << endl;
    cout << &iter << endl;
  }

  // cout << vec1.at(10);
  // cout << vec1[10]; never use

  // testing set
  cout << "testing set " << endl;
  for (auto iter = s.begin(); iter != s.end(); ++iter) {
    cout << *iter << endl;
    cout << &iter << endl;
  }
  for (auto iter : s) {
    cout << iter << endl;
    cout << &iter << endl;
  }
  for (auto &iter : s) {
    cout << iter << endl;
    cout << &iter << endl;
  }

  auto iter = s.find(3);
  cout << *iter << endl;

  cout << *s.lower_bound(3) << endl;

  // testing map
  m.insert(std::make_pair("wuyuheng", 10));
  m.insert(std::make_pair("yuhengwu", 20));
  for (auto &[first, second] : m) {
    cout << first << second << endl;
  }
  for (auto &iter : m) {
    cout << iter.first << iter.second << endl;
  }

  std::vector<int> v{3};
  for (auto &iter : v) {
    cout << iter << endl;
  }

  return 0;
}
