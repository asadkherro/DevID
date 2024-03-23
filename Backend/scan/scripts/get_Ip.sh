#!/bin/bash
# The full ipv4 address with subnet

interface=${1:-"eth0"}
scanFlags=${2:-"-n -sn"}

fullAddr=$(ip addr show $interface | grep -w inet | awk '{print $2}')
machineAddr=$(awk -F / '{print $1}' <<< $fullAddr)
subnetSize=$(awk -F / '{print $2}' <<< $fullAddr)

# The nmap scan target which is the range of the whole subnet
rangeAddr=$(sed -E 's/[0-9]{1,3}$/0/g' <<< $machineAddr)/$subnetSize
echo $rangeAddr
