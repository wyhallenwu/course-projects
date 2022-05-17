#include <algorithm>
#include <functional>
#include <iostream>
#include <memory>
#include <numeric>
#include <string>
#include <vector>
using std::cout;
using std::endl;
using std::string;

// smart pointer
// unique_ptr
// shared_ptr
// weak_ptr

class Node {
 private:
  string data_;
  std::vector<int> vec_;

 public:
  Node(string data = "none") : data_(data) {}
  friend std::ostream &operator<<(std::ostream &out, const Node &node) {
    out << "data: " << node.data_ << endl << "vector: " << endl;
    for (auto &i : node.vec_) {
      out << i << " ";
    }
    out << endl;
    return out;
  }
  void push_back(int val) { this->vec_.push_back(val); }
  int compute() {
    return std::accumulate(this->vec_.begin(), this->vec_.end(), 0);
  }
  friend Node operator+(const Node &n1, const Node &n2) {
    Node n{n1};
    std::transform(n1.vec_.begin(), n1.vec_.end(), n2.vec_.begin(),
                   n.vec_.begin(),
                   [](int i1, int i2) -> int { return i1 + i2; });
    return n;
  }
};

int main() {
  std::unique_ptr<Node> n{std::make_unique<Node>("wuyuheng")};
  n->push_back(1);
  (*n).push_back(2);
  cout << *n << endl;
  cout << n.get() << endl;
  std::unique_ptr<Node> s = std::move(n);
  cout << *s << endl;
  cout << s.get() << endl;
  cout << "weak_ptr" << endl;
  auto s1 = std::make_shared<Node>("yuhengwu");
  std::weak_ptr<Node> w = s1;
  auto w1 = w.lock();
  cout << *w1 << endl;
  return 0;
}