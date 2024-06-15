#!/bin/bash

# Check if user has sudo privileges
if [ $(id -u) -ne 0 ]; then
    echo "Please run this script with sudo or as root."
    exit 1
fi

# Check if nmap is installed
if ! command -v nmap &> /dev/null; then
    echo "nmap is not installed. Please install it first."
    exit 1
fi

# Check if target IP is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <target_IP>"
    exit 1
fi

target_ip=$1

# Run nmap with smb-os-discovery script
echo "Running nmap smb-os-discovery script on target IP: $target_ip ..."
sudo nmap -O --osscan-guess $target_ip
