#include <iostream>
#include "PCB_block.h"
#include "PSA_api.h"
using namespace std;

PCB_queue::~PCB_queue(){
    PCB *p = head;
    while(head != rear)
    {
        head = head -> get_next();
        delete p;
        p = head;
    }
    delete p;
}

void PCB_queue::insert(PCB *&pcb_){
    pcb_ -> get_next() = head -> get_next();
    head = pcb_;
}