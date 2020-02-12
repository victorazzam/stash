#!/usr/bin/env bash

tshark -r mysite.pcap -q -z follow,tcp,ascii,1 | grep flag | cut -d= -f3 | sed -e 's/%7B/{/' -e 's/%7D/}/'
