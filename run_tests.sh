#!/bin/bash
python -OO -m unittest -v\
    tests.ship_guns\
    tests.attack_simulations

if [ $? != 0 ]; then
{
    echo -e "\n\n\e[1;31m+----------------------------------+\e[0m"
    echo -e "\n\n\t\e[1;31mTests failed. Fix them kthx!\e[0m"
    echo -e "\n\n\e[1;31m+----------------------------------+\e[0m"
    exit 1
} else
{
    echo -e "\n\n\e[1;32;40m+------------------------------+\e[0m"
    echo -e "\n\n\t\e[1;32;40mTests passed. Good job!\e[0m"
    echo -e "\n\n\e[1;32;40m+------------------------------+\e[0m"
    exit 0
} fi
