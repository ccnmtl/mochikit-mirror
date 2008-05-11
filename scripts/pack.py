#!/usr/bin/env python
#
# custom_rhino.jar from:
#   http://dojotoolkit.org/svn/dojo/buildscripts/lib/custom_rhino.jar
#
import os
import re
import sys
import shutil
import subprocess
dirname = os.path.dirname(os.path.dirname(__file__))
mk = file(os.path.join(dirname, 'MochiKit/MochiKit.js')).read()
if len(sys.argv) > 1:
    outf = sys.stdout
else:
    outf = file(os.path.join(dirname, 'packed/MochiKit/MochiKit.js'), 'w')
VERSION = re.search(
    r"""(?mxs)MochiKit.MochiKit.VERSION\s*=\s*['"]([^'"]+)""",
    mk
).group(1)
if len(sys.argv) > 1:
    SUBMODULES = sys.argv[1:]
else:
    SUBMODULES = map(str.strip, re.search(
        r"""(?mxs)MochiKit.MochiKit.SUBMODULES\s*=\s*\[([^\]]+)""",
        mk
    ).group(1).replace(' ', '').replace('"', '').split(','))
    SUBMODULES.append('MochiKit')
alltext = '\n'.join(
    [file(os.path.join(dirname, 'MochiKit/%s.js' % m)).read() for m in SUBMODULES])

tf = file(os.path.join(dirname, 'packed/_scratch.js'), 'w')
tf.write(alltext)
tf.flush()
p = subprocess.Popen(
    ['java', '-jar', os.path.join(dirname, 'scripts/custom_rhino.jar'), '-c', tf.name],
    stdout=subprocess.PIPE,
)
print >>outf, """/***

    MochiKit.MochiKit %(VERSION)s : PACKED VERSION

    THIS FILE IS AUTOMATICALLY GENERATED.  If creating patches, please
    diff against the source tree, not this file.

    See <http://mochikit.com/> for documentation, downloads, license, etc.

    (c) 2005 Bob Ippolito.  All rights Reserved.

***/
""" % locals()
shutil.copyfileobj(p.stdout, outf)
outf.write('\n')
outf.flush()
outf.close()
tf.close()
os.remove(tf.name)
