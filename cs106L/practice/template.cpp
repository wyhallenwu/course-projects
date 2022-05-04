#include <iostream>
#include <string>
#include <vector>

using std::string;
using std::cin;
using std::cout;
using std::endl;

template <typename T>
bool isLessThan(T value, T order){
    return { value < order};
}


int main(){
    std::vector<int> vec{1, 2, 3, 5, 4};
    for(auto iter=vec.begin(); iter!=vec.end(); ++iter){
        cout << isLessThan<int>(*iter, 3) << endl;
    }
    // using lambda
    int order = 10;
    auto isLargerThan = [order](auto value){return value > order;};
    for(auto iter=vec.begin(); iter!=vec.end(); ++iter){
        cout << isLargerThan(*iter) << endl;
    }
    return 0;
}
