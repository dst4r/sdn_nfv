#!/bin/bash
# creates namespace and assign it to br0
sudo ip netns add peach
sudo ip netns add bowser

# Add two veth interfaces
sudo ip link add peach2net type veth peer name net2peach
sudo ip link add bowser2net type veth peer name net2bowser

# Assign interface to network namespace
sudo ip link set peach2net netns peach
sudo ip link set bowser2net netns bowser

# Assign IP address to the interface on bowser namespace
sudo ip netns exec peach ip a add 10.64.2.2/24 dev peach2net
sudo ip netns exec bowser ip a add 10.64.2.3/24 dev bowser2net

# Bring the interface up
sudo ip netns exec peach ip link set dev peach2net up
sudo ip netns exec bowser ip link set dev bowser2net up

# Bring the loopback up
sudo ip netns exec peach ip link set dev lo up
sudo ip netns exec bowser ip link set dev lo up

# Verify the links
sudo ip netns exec peach ip -c link
sudo ip netns exec bowser ip -c link

# Create a bridge
sudo ip link add name br0 type bridge

# Assign interfaces to the bridge
sudo ip link set dev net2peach master br0
sudo ip link set dev net2bowser master br0

# Install bridge-utils
sudo apt install bridge-utils

# Verify bridge
brctl show

# Bring up the bridge interface
sudo ip link set dev br0 up

# verify the interfaces in the bridge
bridge link show br0

# DONE
