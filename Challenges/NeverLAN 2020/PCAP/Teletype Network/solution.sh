#!/usr/bin/env bash

strings telnet.pcap | egrep -o 'flag\{.{0,30}'
