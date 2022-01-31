#include <unistd.h>

#include <iostream>

#include "lru.h"
using namespace std;

int main() {
  Instructions l(6);
  l.show_seq();

  Lru lru(3);
  for (int i = 0; i < l.getseq().size(); i++) {
    cout << "current " << i << endl;
    lru.pipeline(l.getseq()[i]);
  }
  cout << "END" << endl;

  return 0;
}