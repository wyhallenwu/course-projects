#include <iostream>
#include <string>
#include <vector>

using namespace std;

// class
//
// basic
//
class Student {
private:
  std::string name_;
  int id_;
  std::string department_;
  std::vector<float> grades;

public:
  // constructors
  Student(std::string name = "none", int id = 0,
          std::string department = "none");
  // copy constructors
  Student(const Student &student) noexcept;
  // copy assignment
  Student& operator=(const Student &student);
  // destructor
  // virtual ~Student();

  //operator<<
  friend ostream& operator<<(ostream& out, const Student& student);
  void SetGrade(const vector<float>& grade);
};
