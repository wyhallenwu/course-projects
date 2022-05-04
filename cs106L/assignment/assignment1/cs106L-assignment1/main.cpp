#include "wikiscraper.h" // wikiscraper methods
#include <filesystem>    // making inputting files easier
#include <fstream>       // for ifstream
#include <iostream>      // for cout, cin
#include <queue>
#include <sstream> // for stringstream
#include <unordered_map>
#include <unordered_set> // containers for the wikiscraper
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::ifstream;
using std::priority_queue;
using std::string;
using std::stringstream;
using std::unordered_map;
using std::unordered_set;
using std::vector;

int main() {
  // a quick working directory fix to allow for easier filename inputs
  auto path = std::filesystem::current_path() / "res/";
  std::filesystem::current_path(path);
  std::string filenames = "Available input files: ";
  for (const auto &entry : std::filesystem::directory_iterator(path)) {
    std::string filename = entry.path().string();
    filename = filename.substr(filename.rfind("/") + 1);
    filenames += filename + ", ";
  }
  // omit last ", ".
  cout << filenames.substr(0, filenames.size() - 2) << "." << endl;

  /* Container to store the found ladders in */
  vector<vector<string>> outputLadders;

  cout << "Enter a file name: ";
  string filename;
  getline(cin, filename);

  /*
      TODO: Create a filestream from the filename.
      For each pair {start_page, end_page} in the input file,
      retrieve the result of findWikiLadder(start_page, end_page)
      and append that vector to outputLadders.
  */
  // Write code here
  ifstream ifs(filename, ifstream::in);
  int pairNum;
  string start, end;
  ifs >> pairNum;
  for (int i = 0; i < pairNum; ++i) {
    string line;
    ifs >> start >> end;
    outputLadders.push_back(findWikiLadder(start, end));
  }
  /*
   * Print out all ladders in outputLadders.
   * We've already implemented this for you!
   */
  // Write code here
  for (auto &ladder : outputLadders) {
    if (ladder.empty()) {
      cout << "no ladder" << endl;
    } else {
      cout << "ladder: " << endl;
      std::copy(ladder.begin(), ladder.end() - 1,
                std::ostream_iterator<string>(cout, ", "));
      cout << ladder.back() << endl;
    }
  }

  return 0;
}
