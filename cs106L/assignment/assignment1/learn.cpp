#include <iostream>
#include <fstream>
#include <sstream>


using std::cout;
using std::cin;
using std::string;


int main(){
	string filename;
	cout << "please input file name." << std::endl;
	cin >> filename;
	std::fstream ifs;
	ifs.open(filename, std::ios::in);
	int num;
	ifs >> num;	
	cout << "the number of all nodes is: " << num << std::endl;	
	string t, d;
	while(ifs >> t >> d){
		cout << t << "  " << d << std::endl;
	}
	// using getline()
	ifs.close();
	ifs.open(filename.c_str(), std::ios::in);
	if(!(ifs.is_open())){
		std::cerr << "file open error" << std::endl;
	}
	ifs >> num;
	string line;
	int count = 0;
	while(std::getline(ifs, line)){ 
		cout << line << std::endl;
		cout << count << std::endl;
		count++;
	}
	ifs.close();
	return 0;
}
