#include <iostream>
#include <memory>
#include <string>
using std::cout;
using std::endl;

class Node {
private:
  std::string data_;
  std::string info_;

public:
  Node(std::string data = "none", std::string info = "none")
      : data_(data), info_(info) {}
  virtual ~Node(){}
  friend std::ostream& operator<<(std::ostream& out, const std::shared_ptr<Node>& uptr){
      out << &uptr << endl;
      out << "data: " << uptr->data_<< " info: " << uptr->info_ << endl;
      return out;
  }
};


int main(){
    std::shared_ptr<Node> n = std::make_shared<Node>("wuyuheng", "yuhengwu");
    cout << &n << endl;
    cout << n;
    return 0;
}
