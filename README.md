# www_byline
Allow browsing of directory structure and files with line-numbering on flat ASCII files

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

    AliasMatch ^/~user/(for_pds/pds_p2)/byline/.*[.](asc|cat|lbl|tab|txt)$ /home/user/public_html/$1/cgi-bin/pds_byline.cgi

    UserDir public_html

    <Directory /home/user/public_html/>
        #Loadmodule authn_google_module modules/mod_authn_google.so
        AllowOverride All
    </Directory>


cgi-bin/.htaccess

- Prevents Index listing by WWW server of ./cgi-bin/ directory
- Allows scripts named *.cgi in ./cgi-bin/ directory to execute


cgi-bin/pds_byline.cgi

- Filter to prepend seven-digit, zero-padded line numbers to flat ASCII
  files; file names come from REQUEST_URI, and the path to a file is
  ../${REQUEST_URI}
