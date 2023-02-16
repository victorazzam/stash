G='\x1b[92;1m'
Z='\x1b[m'

cd /usr/local/src/nginx
echo -en "${G}Working directory:${Z} "
pwd

echo -en "${G}Downloading nginx source"
sleep 0.5
echo -n .
sleep 0.5
echo -n .
sleep 0.5
echo -en ".${Z}"
apt source nginx >/dev/null 2>&1
echo ' Done'

version=$(nginx -v 2>&1 | cut -d/ -f2)
cd "nginx-${version}"

echo -e "${G}Configuring module${Z}"
./configure --with-compat --with-openssl=/usr/include/openssl/ --add-dynamic-module=/usr/local/src/ModSecurity-nginx

echo -e "${G}Building module${Z}"
make modules

echo -e "${G}Copying module to /usr/share/nginx/modules${Z}"
cp objs/*modsecurity*.so /usr/share/nginx/modules/

echo -e "${G}Script completed!${Z}"
