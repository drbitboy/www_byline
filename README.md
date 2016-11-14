# www_byline
Enable Apache HTTPd server to display directory structure and files with line-numbering on flat ASCII files


#How-to example:

http://pdssbn.astro.umd.edu/holdings/ as http://pdssbn.astro.umd.edu/byline/holdings/

0) Assume that holdings/ directory is in /home/www/top/holdings/

0.1) Assume all holdings/-related configuration is in /etc/httpd/conf.d/holdings.conf

1) Add the following lines to /etc/httpd/conf.d/holdings.conf:

    AliasMatch ^/byline/holdings/.*[.](asc|cat|lbl|tab|txt)$ /home/www/top/holdings/cgi-bin/pds_byline.cgi

    <Directory /home/www/top/holdings/cgi-bin>
        AllowOverride All
    </Directory>

2) CHDIR to the top of this repo

2.1) rsync -av byline cgi-bin /home/www/top/holdings/

3) Reload Apache HTTPd server e.g.

     service httpd reload

   or

     service apache reload


#Manifest

byline

- Symlink to .
- Allows WWW clients to browse ./whatever... tree vai byline/whatever...
  in the typical directory Apache Index fashion, with the exception that
  files defined via AliasMatch in /etc/httpd/conf.d/whatever.conf are
  passed to ./cgi-bin/pds_byline.cgi


/etc/httpd/conf.d/something.conf

  or

/etc/httpd/conf/httpd.conf

- Apache HTTPd configuration file
- Not part of this repository, but contains lines like these:

    AliasMatch ^/byline/holdings/.*[.](asc|cat|lbl|tab|txt)$ /cgi-bin/pds_byline.cgi

    <Directory /cgi-bin>
        AllowOverride All
    </Directory>


cgi-bin/.htaccess

- Prevents Index listing by WWW server of ./cgi-bin/ directory
- Allows script named pds_byline.cgi in ./cgi-bin/ directory to execute
- Assumes AllowOverride All for cgi-bin/ directory has been configured
  - See previous comment


cgi-bin/pds_byline.cgi

- Filter to prepend per-line anchors and seven-digit, zero-padded line
  numbers to flat ASCII files; file names come from REQUEST_URI, and
  the path to a file is ../${REQUEST_URI}
