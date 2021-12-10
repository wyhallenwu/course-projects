#ifndef _PSA_BLOCK_H_
#define _PSA_BLOCK_H_

/**
 * @brief 
 * this is the realization of file PSA_api.h
 */

#include <iostream>
using namespace std;
#include "PSA_api.h"

//================== PCB block API ============

PCB*& PCB::get_next()
{
    return this->next;
}

int PCB::gpid()
{
    return this->pid;
}

int PCB::get_priority()
{
    return this->priority;
}

int PCB::get_all_runtime()
{
    return this->all_runtime;
}

int PCB::get_cpu_time()
{
    return this->cpu_time;
}

status PCB::get_status()
{
    return this->process_status;
}

bool PCB::execute(int time_clip_ = 2){
    if(!this -> exec_permission())
        return false;
    this -> status_change(RUNNING);
    status status_ = this -> cpu_time_change(time_clip_);
    this -> status_change(status_);
}

//===================PCB block API helper================

void PCB::status_change(status status_)
{
    this->process_status = status_;
}

status PCB::cpu_time_change(int time_clip = 2)
{
    int tem_time = this -> get_cpu_time() + time_clip;
    if (tem_time <= this -> all_runtime)
    {
        this -> cpu_time = tem_time;
        this -> priority_change();
        return BLOCKING;
    }
    else
    {
        this -> cpu_time = this -> all_runtime;
        this -> priority_change();
        return FINISHED;
    }
}

bool PCB::priority_change(int reduce = 3){
    if(this -> priority > 3)
        this -> priority -= 3;
    else
        this ->priority = 0;

}

bool PCB::exec_permission(){
    if(this -> process_status == READY)
        return true;
    return false;
}


//**********************PCB queue*****************************


void PCB_queue::print_all_info() const
{
    PCB *p = head;
    cout<<"running process is: "<<p -> gpid()<<endl;
    while(p != NULL){
        print_single_info(p);
        p = p -> get_next();
    }
}

void PCB_queue::print_single_info(PCB *&pcb_) const
{
    cout<<pcb_ -> gpid()<<"  "<<pcb_ -> get_priority()<<" "<<pcb_ -> get_all_runtime()
    <<" "<<pcb_ -> get_cpu_time()<<"  "<<pcb_ -> get_status()<<endl;
}

void PCB_queue::insert(PCB *&pcb_)
{
    PCB *p = head;
    PCB *f = NULL;
    while(p -> get_priority() > pcb_ ->get_priority()){
        f = p;
        p = p -> get_next();
    }
    f -> get_next() = pcb_;
    pcb_ -> get_next() = p;
}
#endif