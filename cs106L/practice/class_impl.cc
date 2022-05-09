#include "class.h"
#include <iostream>
#include <iterator>
#include <string>
#include <vector>
using namespace std;

Student::Student(string name, int id, string department):name_(name), id_(id), department_(department){}

Student::Student(const Student& student) noexcept:name_(student.name_), id_(student.id_), department_(student.department_){}

Student& Student::operator=(const Student& student){
    if(this!=&student){
        this->name_ = student.name_;
        this->id_ = student.id_;
        this->department_ = student.department_;
        this->grades = student.grades;
    }
    return *this;
}

ostream& operator<<(ostream& out, const Student& student){
    out << "name: " << student.name_ << " id: " << student.id_ << "  department: " << student.department_ << endl;
    std::copy(student.grades.begin(), student.grades.end(), std::ostream_iterator<float>(out, ", "));
    out << endl;
    return out;
}

void Student::SetGrade(const vector<float>& grade){
    this->grades = grade;
}

int main(){
    Student s1{"yuhengwu", 1, "cs"};
    Student s2;
    cout << s1 << s2;
    s1.SetGrade(vector<float>{10, 20 ,30, 50.5});
    s2 = s1;
    cout << s1 << s2;
    return  0;
}
