#include <iostream>
#include <string>
using namespace std;

class Time{
    private:
        string hour_;
        string minute_;
        string second_;
    public:
        Time(string hour="--", string minute="--", string second="--"):hour_(hour), minute_(minute), second_(second){}
        // operator overload
        // copy assignment
        Time& operator=(const Time& time){
            this->hour_ = time.hour_;
            this->minute_ = time.minute_;
            this->second_ = time.second_;
            return *this;
        }
        // + hour, minute, second
        friend Time operator+(const Time& time, const Time& add);
        bool IsTimeLegal() const {
            if(this->hour_=="--" || this->minute_ == "--" || this->second_=="--") return false;
            return true;
        }
        friend ostream& operator<<(ostream& out, const Time& time){
            out << time.hour_ << ":" << time.minute_ << ":" << time.second_ << endl;
            return out;
        }

        // +=
        Time& operator+=(const Time& time){
            if(this->IsTimeLegal() && time.IsTimeLegal()){
                // not a good impl
                *this = *this + time;
                return *this;
            }
            throw "not a legal time format";
        }
        
};

Time operator+(const Time& time, const Time& add){
    if(time.IsTimeLegal() && add.IsTimeLegal()){
        Time result = time;
        result.hour_ = to_string(stoi(result.hour_) +stoi(add.hour_));
        result.minute_ = to_string(stoi(result.minute_) +stoi(add.minute_));
        result.second_ = to_string(stoi(result.second_) + stoi(add.second_));
        return result;
    }
    throw "not a legal time format";
}


int main(){
    Time t1{"12", "20", "30"};
    Time t2{"2", "10", "10"};
    cout << t1  << t2 ;
    cout << t1 + t2;
    cout << &t1 << endl;
    t1 += t2;
    cout << &t1 <<endl;
    cout << t1;
    return 0;
}
