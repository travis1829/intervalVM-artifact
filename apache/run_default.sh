
PREFIX="/usr/local/apache2"
CPUS="${CPUS:-64}"
MAX_CPUS=$(nproc)

sudo cp index_64KB.html $PREFIX/htdocs/index.html
sudo cp httpd.conf $PREFIX/conf/httpd.conf
sudo cp httpd-mpm-default.conf $PREFIX/conf/extra/httpd-mpm.conf

sudo $PREFIX/bin/apachectl -k stop
sudo $PREFIX/bin/apachectl -k start

./wrk/wrk -t$MAX_CPUS -c100 -d10s http://localhost/

sudo $PREFIX/bin/apachectl -k stop
