#include <iostream>
#include <string>
#include <algorithm>
using namespace std;
using std::string;

int main(){
    string s{"there will rain willwill ."};
    string pattern{"will"};
    auto start = s.begin();
    while(true){
        auto link = std::search(start, s.end(), pattern.begin(), pattern.end());
        if (link == s.end()){
            break;
        }
        cout << string(link, link+pattern.length()) << endl;
        start += pattern.length();
    }
    auto end = std::find(s.begin(), s.end(), 'w');
    cout << string(s.begin(), end);
    if(!false){
        cout << "w";
    }
    return 0;
}