#!/bin/bash
f450_num=3

vehicle_num=0
while(( $vehicle_num< f450_num)) 
do
    python multirotor_communication.py f450 $vehicle_num&
    let "vehicle_num++"
done
