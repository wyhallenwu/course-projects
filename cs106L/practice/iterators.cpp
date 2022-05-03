#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

using namespace std;
using std::vector;

int main() {
  vector<int> vec1{1, 2, 3, 4, 5};
  cout << "using for each expression" << endl;
  for (auto data : vec1) {
    cout << data << "  ";
    cout << &data << "  ";
    // change data to 10 not effective
    data = 10;
  }
  cout << endl;
  cout << "using for each with auto&" << endl;
  for(auto& data : vec1){
      cout << data << "  ";
      cout << &data << "  ";
      // change data to 10
      data = 10;
  } 
  cout << endl;

  cout << "using iterators" << endl;
  for (auto iter = vec1.begin(); iter != vec1.end(); ++iter) {
    cout << *iter << " ";
    cout << &(*iter) << "  ";
  }
  cout << endl;
  cout << "using random access of vector" << endl;
  for(auto i=0; i < vec1.size(); ++i){
      cout << vec1.at(i) << "  ";
      cout << &vec1.at(i) << "  ";
  }
  cout << endl;

  return 0;
}
