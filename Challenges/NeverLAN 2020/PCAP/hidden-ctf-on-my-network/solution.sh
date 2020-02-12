#!/usr/bin/env bash

tshark -r hidden-ctf-on-my-network/connect-to-bashNinjas-network.pcapng -q -z follow,udp,ascii,3 | grep flag | cut -d. -f6 | tr -d 6
