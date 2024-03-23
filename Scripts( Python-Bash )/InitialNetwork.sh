#!/bin/bash

# The interface from which to take the address and subnet
interface=${1:-"wlan0"}

# Get the nmap scan flags from second argument that must be enclosed with quotes
scanFlags=${2:-"-n -sn"}

# The full ipv4 address with subnet
fullAddr=$(ip addr show $interface | grep -w inet | awk '{print $2}')
machineAddr=$(awk -F / '{print $1}' <<< $fullAddr)
subnetSize=$(awk -F / '{print $2}' <<< $fullAddr)

# The nmap scan target which is the range of the whole subnet
rangeAddr=$(sed -E 's/[0-9]{1,3}$/0/g' <<< $machineAddr)/$subnetSize

# Show execution details which can be useful to know machine ip and subnet
printf "Running subnet scan custom script.\n\n"
printf "Your machine IPv4 address is: "$machineAddr", the subnet size is: /"$subnetSize"\n"
printf "The scan range will be the whole subnet: "$rangeAddr" and your IPv4 will be excluded.\n"
printf "By default it will perform a simple Ping Scan to detect active hosts on network.\n"
printf "You can customize the scan flags passing as the second argument enclosed by quotes\n"
printf "the first argument is the interface you want to use to get the address.\n\n"

# Print few usage examples
printf "For example:\n"
printf "scan-subnet wlan0 \"-n -A -T4\"\n"
printf "scan-subnet eth0 \"-n -O -sV -F\"\n"

printf "\nRunning the scan with nmap the output will be shown here: \n"

# Run the actual scan on the whole subnet excluding the machine ip
nmap $scanFlags --exclude $machineAddr $rangeAddr
