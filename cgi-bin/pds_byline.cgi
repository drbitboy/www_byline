#!/usr/bin/env python
import re,os,sys,cgitb
cgitb.enable()
request_uri,uriPrefix = os.environ["REQUEST_URI"],r'/~user/for_pds/pds_p2/byline/'
assert re.compile(r'^%sdata_sets/20\d\d\d\d\d\d/nh-[jpx]-[a-z]*-[23]-[a-z]*-v[0-9.]*/[a-z0-9_/]*[.](asc|cat|lbl|tab|txt)$'%(uriPrefix,)).match(request_uri)
with open(os.path.join('..',request_uri[len(uriPrefix):]),'rb') as fInp:
  sys.stdout.write("""Content-type:  text/html\n\n<html><style>body { white-space: pre; font-family: "Courier New", Monospace; }</style><body>""")
  lineOrdinal = 0
  for rawline in fInp:
    lineOrdinal += 1
    sys.stdout.write('<a id="line_%d" />%07d:%s\n' % (lineOrdinal,lineOrdinal,rawline.rstrip().replace('<','&lt;').replace('>','&gt;'),))
sys.stdout.write("</body></html>\n")
