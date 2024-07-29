#!/bin/bash

# Get current device IP addresses
ip_addr=$(ip addr show | grep -w inet | grep -v 127.0.0.1 | awk '{print $2}')

# Extract Operating System and Kernel Name
os_name=$(hostnamectl | grep "Operating System" | awk -F: '{print $2}' | xargs)
kernel_name=$(hostnamectl | grep "Kernel" | awk -F: '{print $2}' | xargs)

# Get the subnet using provided code
interface=${1:-"eth0"}

# Check if interface exists and has an IP address
if ! ip addr show $interface > /dev/null 2>&1; then
    echo "Error: Interface $interface does not exist."
    exit 1
fi

fullAddr=$(ip addr show $interface | grep -w inet | awk '{print $2}')
if [ -z "$fullAddr" ]; then
    echo "Error: No IP address found for interface $interface."
    exit 1
fi

machineAddr=$(awk -F / '{print $1}' <<< $fullAddr)
subnetSize=$(awk -F / '{print $2}' <<< $fullAddr)

# The nmap scan target which is the range of the whole subnet
rangeAddr=$(sed -E 's/[0-9]{1,3}$/0/g' <<< $machineAddr)/$subnetSize

# Echo the details
echo "IP Addresses: $ip_addr"
echo "Operating System: $os_name"
echo "Kernel Name: $kernel_name"
echo "Subnet: $rangeAddr"
