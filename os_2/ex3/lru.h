#include <deque>
#include <iostream>
using namespace std;

struct page {
  int _page_num;
  int _cache_block;
  int _access_count;
  page() {
    srand(unsigned(time(0)));
    _page_num = rand() % 10 + 1;
    _access_count = 0;
    _cache_block =
        -1;  // -1 means the page is currently stored in external memory
  }
  page(int page_num) : _page_num(page_num) {
    _access_count = 0;
    _cache_block = -1;
  }

  void show_info() {
    cout << "page number: " << _page_num << " | cache block: " << _cache_block
         << " | access count: " << _access_count << endl;
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

class Lru {
 private:
  deque<page> _list;
  int _size;

 public:
  Lru(int size) : _size(size) {
    _list = deque<page>(size);
    _list.clear();
    cout << "capacity is: " << _size << endl;
  }

  deque<page>& getlist() { return _list; }
  int getsize() { return _size; }

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

  int find_lr() {
    int max_index = 0;
    for (int i = 0; i < _size; i++) {
      if (_list[i]._access_count > _list[max_index]._access_count)
        max_index = i;
    }
    return max_index;
  }

  void round_end() {
    for (int i = 0; i < _list.size(); i++) _list[i]._access_count += 1;
  }

  void exchange(page& page_toinsert) {
    int index = find_lr();
    _list[index] = page_toinsert;
    _list[index]._cache_block = index;
  }

  void show_all() {
    cout << "lru: " << endl;
    for (int i = 0; i < _list.size(); i++) {
      _list[i].show_info();
    }
    cout << endl;
  }

  void reuse(int page_num) {
    for (int i = 0; i < _list.size(); i++) {
      if (_list[i]._page_num == page_num) {
        _list[i]._access_count = 0;
      }
    }
  }

  void add(page& page_todeal) {
    _list.push_back(page_todeal);
    _list.back()._cache_block = _list.size() - 1;
  }

  void pipeline(page& page_todeal) {
    if (!isFull() && !isIn(page_todeal._page_num)) {
      add(page_todeal);

    } else if (isFull() && !isIn(page_todeal._page_num)) {
      exchange(page_todeal);
    } else {
      reuse(page_todeal._page_num);
    }
    round_end();
    show_all();
  }
};