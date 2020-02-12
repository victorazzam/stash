#!/usr/bin/env bash

strings ftp.pcap | egrep -o 'flag\{.{0,30}'
