#!/usr/bin/env bash
# All hints are in /home/User/.bash_history

tar xzf look_into_the_past.tar.gz
dir="look_into_the_past"
tar xzf $dir/opt/table.db.tar.gz -C $dir/opt

pass1=$(steghide extract -q -p '' -sf $dir/home/User/Pictures/doggo.jpeg && cat stegano* && rm stegano*)
pass2=$(tail -1 $dir/etc/shadow | cut -d':' -f2)
pass3=$(sqlite3 $dir/opt/table.db 'SELECT * FROM passwords;' | cut -d'|' -f2)
# $pass1 = JXrTLzijLb
# $pass2 = KI6VWx09JJ
# $pass3 = nBNfDKbP5n

openssl enc -aes-256-cbc -salt -in $dir/home/User/Documents/flag.txt.enc -k JXrTLzijLbKI6VWx09JJnBNfDKbP5n -d | xargs
rm -rf look_into_the_past
