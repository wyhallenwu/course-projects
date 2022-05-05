#include <iostream>
#include <string>
#include <vector>
#include <functional>

using std::string;
using std::cin;
using std::cout;
using std::endl;

template <typename T>
bool isLessThan(T value, T order){
    return { value < order};
}

// typename and class are the same
template <class T>
auto min(T v1, T v2){
    return v1 < v2 ? v1 : v2;
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
    for(auto iter = vec.begin(); iter!= vec.end(); ++iter){
        cout << *iter <<endl;
    }
    
    // testing functors
    std::function<bool(int)> func = isLargerThan;
    if(func(20)){
        cout << "the type of lambda is std::function" <<endl;
    }
    std::function<bool(float)> func2 = isLargerThan;
    if(func2(10.5)){
        cout << "the type of lambda's parameter list should be defined" << endl;
    }

    cout << min<int>(10, 20) << endl;
    cout << min(9.5, 10.5) << endl;

    int a =10;
    cout << &a << endl;
    const int& c = a;
    cout << c << endl;
    cout << &c << endl;
    a += 10;
    cout << c << endl;
    return 0;
}
