#include "BankersAlgorithm.h"

int main() {
  vector<int> p1_need{1, 2, 3};
  vector<int> p2_need{2, 3, 1};
  vector<int> p3_need{0, 4, 1};
  vector<int> max{4, 4, 4};

  Process p1(p1_need, max);
  Process p2(p2_need, max);
  Process p3(p3_need, max);
  cout << p1;

  vector<int> available{3, 5, 2};
  vector<int> allcation{0, 0, 0};

  BankersAlgorithm test(available, allcation);
  test.process_coming(p1);
  test.process_coming(p2);
  test.process_coming(p3);
  cout << test;
  vector<int> consume{1, 1, 1};
  test.pipeline(consume, 0);
  return 0;
}