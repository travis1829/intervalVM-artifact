# Installs apache at the default path (/usr/local/apache2) and wrk at ../apache/wrk.
# To uninstall, remove ../apache/wrk, ../apache/httpd-2.4.62, and /usr/local/apache2

APACHE="../apache"
HTTPD="httpd-2.4.62"
APR="apr-1.7.5"
APR_UTIL="apr-util-1.6.3"

# Requires the following. Note: `apt install` will only work on debian and ubuntu.
# apt install libpcre2-dev libexpat1-dev

cd $APACHE

if [ ! -d "wrk" ]; then
    git clone https://github.com/wg/wrk.git
    make -C wrk
fi

tar -xvf $HTTPD.tar
tar -xvf $APR.tar
tar -xvf $APR_UTIL.tar
mv $APR $HTTPD/srclib/apr
mv $APR_UTIL $HTTPD/srclib/apr-util

cd $HTTPD
./configure --with-included-apr
make
sudo make install
