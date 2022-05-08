#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Person {
private:
  string name;
  int id;

public:
  Person(string name, int id) : name(name), id(id) {}
  Person() : name("none"), id(0) {}
  friend ostream &operator<<(ostream &out, const Person &person);
  bool operator<(const Person &person) { return this->name < person.name; }
  Person &operator+=(const Person &person) {
    this->id += person.id;
    return *this;
  }
  Person operator+(const Person &person1) const {
    Person result(*this);
    result += person1;
    return result;
  }
};

ostream &operator<<(ostream &out, const Person &person) {
  out << person.name << " " << person.id << endl;
  return out;
}

int main() {
  Person person1("wuyuheng", 1);
  cout << person1;
  Person person2("yuheng", 2);
  if (person1 < person2) {
    cout << "operator<" << endl;
  }
  person1 += person2;
  cout << person1;
  // testing operator+
  Person p;
  p = person1 + person2;
  cout << p;
  return 0;
}
