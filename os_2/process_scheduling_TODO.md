## 2021-12-5

- [x] overview of the whole procedure
- [x] draw a map to solve it

**demand**

1. suppose we have N processes to be scheduled. N can increase during the scheduling. 
2. every process has its own PCB in which contains **process_name, process_priority, all_runtime, cpu_runtime, process_status(running, block, ready, finished, building)**  and so on.
3. the system should be able to exhibit the current status of each process and the varied parameters.
4. the  system can use several kinds of scheduling algorithms introduced in the class, such as **priority first, Round-Robin(RR), Multi-level feedback queue(MLFQ)**

***

<1> conceive and design of the system 2021-12-5

language : C++

> 1. PCB -- class: containing {basic information of PCB} and function(){ displaying information}
>
> 2. three algorithms -- three classes: containing {CPU information} and  function(){the basic operations such as process switch, time reducing for single PCB, priority change.}
> 3. two queues (block, ready) -- class: containing {queue attributes} and function(){queue operation, end_detection: block queue and ready queue are both empty, running finished}
>
> MLFQ may need a specific design

