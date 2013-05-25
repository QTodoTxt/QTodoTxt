import os
import fnmatch
import re
import hashlib

baseDir = "/tmp/qtodotxt/"

def makeMd5sums():
    
    excludes = ['DEBIAN','*.pyc']
    excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

    for (root,dirs,files) in os.walk(baseDir):

        dirs[:] = [d for d in dirs if not re.match(excludes,d)]

        #files = [os.path.join(root,f) for f in files]
        files = [f for f in files if not re.match(excludes,f)]

        for fn in files:
            path = os.path.join(root,fn)
            md5 = hashlib.md5(open(path,'rb').read()).hexdigest()
            relativePath = root.replace(baseDir,"",1) + os.sep + fn
            print "%s %s" % (md5,relativePath)


makeMd5sums()
