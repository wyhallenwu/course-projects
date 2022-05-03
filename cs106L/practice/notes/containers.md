## containers

### sequence containers
Simple:  
1. vector   
2. deque  
3. list  
4. tuple  

Adaptors:   
1. stack  
2. queue
3. priority_queue  

### Associative containers
Ordered
1. set  
2. map  
Unordered:  
1. unordered_set  
2. unordered_map  

> map's key can be used for comparision or not.   

## Interators
> how to access containers  
> idea: iteration has an order over elements  
  
std::set::iterator iter = s.begin()  
++iter  
\*iter  
iter!= s.end()  
auto second_iter = iter  
