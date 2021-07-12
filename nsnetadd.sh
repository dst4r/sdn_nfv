#!/bin/bash
# creates namespace and assign it to br0
sudo ip netns add bowser

# Add two veth interfaces
sudo ip link add bowser2net type veth peer name net2bowser

# Assign interface to network namespace
sudo ip link set bowser2net netns bowser

# Assign IP address to the interface on bowser namespace
sudo ip netns exec bowser ip a add 10.64.2.3/24 dev bowser2net

# Bring the interface up
sudo ip netns exec bowser ip link set dev bowser2net up

# Bring the loopback up
sudo ip netns exec bowser ip link set dev lo up

# Verify the links
sudo ip netns exec bowser ip -c link
