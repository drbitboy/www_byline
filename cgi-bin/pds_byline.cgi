#!/usr/bin/env python
"""
Apache HTTPd filter to prepend line-number-based anchors and line
numbers to each line of flat ASCII files under /holdings/, while
still allowing normal browsing of /holdings/ directory tree, all
by browsing /byline/holdings/ instead of /holdings/.

Prerequisites:

1) The filepath /byline is a symlink to .

2) The filpeath /byline is a sibling of directory /holdings

3) A line like this

     Aliasmatch ^/byline/holdings/.*[.](asc|cat|lbl|tab|txt)# /cgi-bin/pds_byline.cgi

   is in the Apache HTTPd server configuration (typically
   /etc/httpd/conf*/*.conf).

4) This script is in directory /cgi-bin/pds_byline.cgi

5) Directory /cgi-bin is a sibling of /holdings, and has configuration
   settings like this

     <Directory /cgi-bin>
       Options -Indexes +ExecCGI
       AddHandler cgi-script cgi
     </Directory>

   or, to use /cgi-bin/.htaccess from repo

     <Directory /cgi-bin>
       AllowOverride All
     </Directory>

"""

########################################################################
import re
import os
import sys

########################################################################
### Setup CGI error traceback logging
import cgitb
cgitb.enable()

########################################################################
### Get REQUEST_URI, which should be /byline/holdings/...,
### and end in one of .asc, .cat, .lbl, .tab or .txt
request_uri = os.environ["REQUEST_URI"]

########################################################################
### The prefix for that URI should be a symlink that points to .
uriPrefix =  r'/byline/'

########################################################################
### Use regex to nsure the URI is valid was passed
### N.B. URI regex is lowercase
### N.B. URI data set ID limited to mission, target(s), instrument,
###      CODMAC level, phase, and version, each delimited by hyphens
### N.B. URI regex does not allow full-stop (.) after data set ID
###      directory name until the final extension
assert re.compile(r'^%sholdings/[a-z_]*-[a-z_]*-[a-z0-9_]*-[2-6]-[a-z0-9_]*-v[0-9.]*/[a-z0-9_/]*[.](asc|cat|lbl|tab|txt)$'%(uriPrefix,)).match(request_uri)

########################################################################
### Open the file pointed to by the path ...
with open(os.path.join('..',request_uri[len(uriPrefix):]),'rb') as fInp:

  ######################################################################
  ### Output HTTP header and inital HTML 
  sys.stdout.write("""Content-type:  text/html

<html><style>
  body {
    white-space: pre;
    font-family: "Courier New", Monospace;
  }
</style><body>""")

  ######################################################################
  ### Initialize line number
  lineOrdinal = 0

  ######################################################################
  ### Loop over lines
  for rawline in fInp:

    ####################################################################
    ### Increment line number
    lineOrdinal += 1

    ####################################################################
    ### Output line with modifications:
    ### - Prefix with anchor
    ### - Prefix with seven-digit, zero-padded line number and a colon
    ### - Strip trailing space (newline, carriage return, spaces)
    ### - Convert any < and > characters to &lt; and &gt; respectively
    sys.stdout.write('<a id="line_%d" />%07d:%s\n' % (lineOrdinal,lineOrdinal,rawline.rstrip().replace('<','&lt;').replace('>','&gt;'),))

########################################################################
### Output final HTML 
sys.stdout.write("</body></html>\n")
