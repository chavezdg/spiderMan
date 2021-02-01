#!/usr/bin/env bash

# "PING ALL KVMS BASH SCRIPT"
# Created by davidc
# Version 1

kvmIPs=$( cat -v kvmIPDefs.py | awk '{ print $3 }' | grep -v "IP" | cut -d '"' -f 2 )
kvmDevNum=0

while [[ "$kvmDevNum" != "48" ]]; do
 for kvmDeviceIP in $kvmIPs; do
  kvmDevNum=$((++kvmDevNum))
  ping -c 1 $kvmDeviceIP | grep -o "Destination Host Unreachable" > noOutput \
  && echo "KVM$kvmDevNum IN $kvmDeviceIP IS [ DOWN ]" \
  || echo "KVM$kvmDevNum IN $kvmDeviceIP IS [ UP ]"
 done
done

