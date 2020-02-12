#!/usr/bin/env bash

tshark -r mysite2.pcap -q -z follow,tcp,ascii,2 | grep flag | tail -1 | cut -d= -f3 | sed -e 's/%7B/{/' -e 's/%7D/}/'
