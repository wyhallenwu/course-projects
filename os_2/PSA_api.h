#ifndef _PAS_AIP_H_
#define _PAS_AIP_H_
/**
 * @brief 
 * this file is all about Processing Scheduling algorithm
 * the detailed realization is in PSA.h
 * 
 */

#include <iostream>
using namespace std;

class PCB_queue
{
private:
    PCB *head;
    PCB *rear;

public:
    //===================== constructor and deconstructor =====================
    PCB_queue()
    {
        head = NULL;
        rear = NULL;
    }

    PCB_queue(int pid_, int priority_, int all_runtime_, int cpu_time_, status process_status_)
    {
        head = new PCB(pid_, priority_, all_runtime_, cpu_time_, process_status_, NULL);
        rear = new PCB;
        head->get_next() = rear;
    }

    virtual ~PCB_queue();

    //**************************************************************************

    //========================= API for PCB queue ==============================

    //print the whole queue's information. The format should follow the example.
    void print_all_info() const;

    // insert a PCB into the queue while keeping the priority sequence(head_large -> rear_tiny).
    void insert();

    //**************************************************************************
};

//status enumeration
enum status
{
    RUNNING,
    BLOCKING,
    FINISHED,
    READY,
    UNBUILD
};

class PCB
{
private:
    int pid;
    int priority;
    int all_runtime;
    int cpu_time;
    status process_status;
    PCB *next;

public:
    //initialize PCB block
    PCB(int pid_, int priority_, int all_runtime_, int cpu_time_, status process_status_, PCB *next)
    {
        pid = pid_;
        priority = priority_;
        all_runtime = all_runtime_;
        cpu_time = cpu_time_;
        process_status = READY;
        next = NULL;
    }

    //default initialization
    PCB()
    {
        pid = priority = all_runtime = cpu_time = 0;
        process_status = UNBUILD;
        next = NULL;
    }

    virtual ~PCB()
    {
        delete next;
        next = NULL;
    }
    //================== get PCB block information============

    PCB *&get_next();
    int gpid();
    int get_priority();
    int get_all_runtime();
    int get_cpu_time();
    status get_status();

    //*********************************************************

    //========================== API ==========================
    bool execute(int time_clip_);

    //*********************************************************

    //========================= API helper ====================
    void status_change(status status_);
    status cpu_time_change(int time_clip);
    bool exec_permission();
};

#endif
