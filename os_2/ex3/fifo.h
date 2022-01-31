#include <unistd.h>

#include <deque>
#include <iostream>
using namespace std;

struct page {
  int _page_num;
  int _cache_block;
  page() {
    srand(unsigned(time(0)));
    _page_num = rand() % 10 + 1;
    _cache_block = -1;  // -1 means the page is still in external memory
  }

  void show_info() {
    cout << "page number: " << _page_num << " | cache block: " << _cache_block
         << endl;
  }
};

class Instructions {
 private:
  deque<page> _seq;
  int _size;

 public:
  Instructions(int size) : _size(size) {
    _seq = deque<page>(size);
    for (int i = 0; i < size; i++) {
      srand(unsigned(time(0)));
      _seq[i]._page_num = rand() % 10 + 1;
      sleep(1);
    }
  }

  deque<page>& getseq() { return _seq; }
  int getsize() { return _size; }

  void show_seq() {
    cout << "instructions sequence: " << endl;
    for (int i = 0; i < _seq.size(); i++) {
      _seq[i].show_info();
    }
    cout << endl;
  }
};

class Fifo {
 private:
  deque<page> _list;
  int _size;

 public:
  Fifo(int size) : _size(size) {
    _list = deque<page>(size);
    _list.clear();
  }

  int getsize() { return _size; }
  deque<page>& getlist() { return _list; }

  void show_all() {
    for (int i = 0; i < _list.size(); i++) {
      _list[i].show_info();
    }
  }

  void add(page& page_todeal) {
    _list.push_back(page_todeal);
    _list.back()._cache_block = _list.size() - 1;
  }

  bool isFull() {
    if (_list.size() < _size)
      return false;
    else
      return true;
  }

  bool isIn(int page_num) {
    for (int i = 0; i < _list.size(); i++) {
      if (_list[i]._page_num == page_num) return true;
    }
    return false;
  }

  void exchange(page& page_todeal) {
    _list.pop_front();
    add(page_todeal);
  }

  void pipeline(page& page_todeal) {
    if (!isFull() && !isIn(page_todeal._page_num)) {
      add(page_todeal);
    } else if (isFull() && !isIn(page_todeal._page_num)) {
      exchange(page_todeal);
    }
    show_all();
  }
};