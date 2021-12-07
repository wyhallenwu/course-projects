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

bool PCB::execute(int time_clip_){
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

status PCB::cpu_time_change(int time_clip)
{
    int tem_time = this -> get_cpu_time() + time_clip;
    if (tem_time <= this -> all_runtime)
    {
        this -> cpu_time = tem_time;
        return BLOCKING;
    }
    else
    {
        this -> cpu_time = this -> all_runtime;
        return FINISHED;
    }
}

bool PCB::exec_permission(){
    if(this -> process_status == READY)
        return true;
    return false;
}
#endif