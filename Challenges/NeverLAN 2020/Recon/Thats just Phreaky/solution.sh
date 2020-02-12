#!/usr/bin/env bash

curl -s https://darknetdiaries.com/episode/1/ | grep flag | awk '{print $2}'
