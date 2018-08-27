#/bin/bash

for n in a b c d e f g h i j k l m n o p q r s t u v w x y z
do
	eval A$n="$n"
done
for n in A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
do
	eval A$n="$n"
done
num=0
for n in a b c d e f g h i j
do
	eval B$n="$num"
	num=$((num+1))
done
Bk=' ';Bl='!';Bm='"';Bn='#';Bo='$';Bp='%';Bq='&';Br="'"
Bs='(';Bt=')';Bu='*';Bv='+';Bw=',';Bx='-';By='.';Bz='/'
Ca=':';Cb=';';Cc='<';Cd='=';Ce='>';Cf='?';Cg='@';Ch='['
Ci='\';Cj=']';Ck='^';Cl='_';Cm='`';Cn='{';Co='|';Cp='}'
Cq='~'