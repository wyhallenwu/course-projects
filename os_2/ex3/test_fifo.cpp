#include <unistd.h>

#include <iostream>

#include "fifo.h"

using namespace std;

int main() {
  Instructions l2(6);
  l2.show_seq();
  Fifo f(3);
  for (int i = 0; i < l2.getseq().size(); i++) {
    cout << "current: " << i << endl;
    f.pipeline(l2.getseq()[i]);
  }
  cout << "END" << endl;
  return 0;
}