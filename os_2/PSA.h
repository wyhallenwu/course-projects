#ifndef _PSA_H_
#define _PSA_H_

/**
 * @brief 
 * this is the priority scheduling algorithms 
 * this file contains: PCB class and its API
 * 1. PCB information:
 *      process index: (int) pid
 *      prority: (int) priority
 *      all runtime: (int) all_runtime
 *      process status: enum status(RUNNING, BLOCKING, FINISHED, BUILDING, READY)
 *      next PCB : struct *next
 */

#include <iostream>
using namespace std;

class PCB_queue{
private:
    PCB *head;
    PCB *rear;
public:

    //===================== constructor and deconstructor =====================
    PCB_queue(){
        head = NULL;
        rear = NULL;
    }

    PCB_queue(int pid_, int priority_, int all_runtime_,int cpu_time_, status process_status_){
        head = new PCB(pid_, priority_, all_runtime_, cpu_time_, process_status_, NULL);
        rear = new PCB;
        head -> get_next() = rear;
    }
    
    virtual ~PCB_queue(){

    }

    //**************************************************************************

    //========================= API for PCB queue ==============================

    //print the whole queue's information. The format should follow the example.
    void print_all_info(){

    }

    // insert a PCB into the queue while keeping the priority sequence(head_large -> rear_tiny).
    void insert(){

    }

    //**************************************************************************
};

//status enumeration
enum status{RUNNING, BLOCKING, FINISHED, READY, UNBUILD};

class PCB{
private:
    int pid;
    int priority;
    int all_runtime;
    int cpu_time;
    status process_status;
    PCB *next;
public:
    //initialize PCB block
    PCB(int pid_, int priority_, int all_runtime_,int cpu_time_, status process_status_, PCB *next){
        pid = pid_;
        priority = priority_;
        all_runtime = all_runtime_;
        cpu_time = cpu_time_;
        process_status = READY;
        next = NULL;
    }
    
    //default initialization
    PCB(){
        pid = priority = all_runtime = cpu_time = 0;
        process_status = UNBUILD;
        next = NULL;
    }

    virtual ~PCB(){
        
    }
//================== get PCB block information============

    PCB*& get_next(){
        return this -> next;
    }

    int gpid(){
        return this -> pid;
    }

    int get_priority(){
        return this -> priority;
    }

    int get_all_runtime(){
        return this -> all_runtime;
    }

    int get_cpu_time(){
        return this -> cpu_time;
    }

    status get_status(){
        return this -> process_status;
    }


//*********************************************************

//========================== API ==========================
    void status_change(status status_){
        this -> process_status = status_;
    }
    
    void cpu_time_change(PCB *&pcb, int time_clip){
        int tem_time = pcb -> get_cpu_time() + time_clip;
        if(tem_time <= pcb -> all_runtime)
            pcb -> cpu_time = tem_time;
        else{
            pcb -> cpu_time = this->all_runtime;
            pcb -> status_change(FINISHED);
        }
    }





//*********************************************************

//========================= API helper ====================
    bool status_examine(){
        
    }


};

#endif