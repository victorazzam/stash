#/usr/bin/python

c = "qwertyuiopasdfghjklzxcvbnm"
for i in c + c.upper(): exec("A{0} = '{0}'".format(i))
for i in range(10): exec("B{} = '{}'".format(chr(97 + i), i))
Bk=' ';Bl='!';Bm='"';Bn='#';Bo='$';Bp='%';Bq='&';Br="'"
Bs='(';Bt=')';Bu='*';Bv='+';Bw=',';Bx='-';By='.';Bz='/'
Ca=':';Cb=';';Cc='<';Cd='=';Ce='>';Cf='?';Cg='@';Ch='['
Ci='\\';Cj=']';Ck='^';Cl='_';Cm='`';Cn='{';Co='|';Cp='}'
Cq='~'

flag = "$AZ$AD$Bc$Ba$Bb$Bi$Cn$AT$Ah$Ae$Bk$AK$Bd $Ay$Ab$Ba$Aa$Ar$Ad$Cl$Ai$As$Cl$Am$Bb$Ag $Ah$At$Ai$Ae$Bh$Bk$At$Ah$Be$An$Bx$At$Ah $Ae$Bv$AP$Ae$An$Cp"

print "".join(globals()[x.strip()] for x in flag.split("$") if x.strip())

# ZD2018{The K3yb0ard_is_m1ghtie7 th4n-the+Pen}