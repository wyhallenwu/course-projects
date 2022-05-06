## stream
convert between data and string representation of data.  
1. ostream: cout(to console)
2. istream: cin(from console)  
    > receive string from a stream and convert it to data
3. ifstream (from file) 
4. ofstream (to file)
5. std::getline(ifstream&, string&)
6. istringstream
7. ostringstream

## initialization
uniform init is to use curly bracket {}  
1. struct: . {}
2. std::pair {}, .first .second, make_pair()
3. std::vector (), {} (3, 5) is to make {5, 5, 5} while {3, 5} is to make {3,5}


## auto
don't overuse auto  

## structure binding
ex:
```cpp
auto p = std::make_pair();
string a = p.first;
int b = p.second;


auto [a, b] = p;

```

## reference 
an alias of the variable.  
be careful: 
1. rvalue can be referenced.    
2. can't declare non-const reference to const variable.  


## containers
vector, deque, list, tuple  


### adaptors
stack, queue, priority_queue

### associative containers
set, map / unordered_set, unordered_map  

## iterators and pointers
how to access to the container.  
iterator has an 'ordering' over element.  
**kinds**: random-access, bidirectional, forward, input, output  
**notice**: difference between iterators and for-each loop
