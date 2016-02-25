import urllib.request
import os
import os.path 
import sys
import tarfile
from shutil import copytree,ignore_patterns,copy,rmtree
from stat import *
import fnmatch
import re
import hashlib
import gzip
from string import Template
from subprocess import call


tmpDir="/tmp/"

def dlTagFromGitHub(version):
    remoteFile = urllib.request.urlopen('https://github.com/QTodoTxt/QTodoTxt/archive/'+version+'.tar.gz')
    contentDisposition=remoteFile.info()['Content-Disposition']
    fileName=contentDisposition.split('=')[1]

    localFile = open(tmpDir+fileName, 'wb')
    localFile.write(remoteFile.read())
    localFile.close()
    return fileName


def uncompressFile(fileName):
    os.chdir(tmpDir)
    bashCmd=" ".join(["tar xzf",tmpDir+fileName,"--exclude-vcs --no-same-permissions"])
    call(bashCmd,shell=True)
    return fileName.rsplit(".",2)[0]

def buildPackageFolder(folderName):
    buildDir=tmpDir+folderName+'_build'
    buildBinDir=buildDir+'/usr/share/qtodotxt/bin/'
    debianDir=buildDir+'/DEBIAN/'

    # Tree structure
    os.makedirs(debianDir)
    os.makedirs(buildDir+'/usr/bin/')
    os.makedirs(buildDir+'/usr/share/doc/qtodotxt')
    os.makedirs(buildDir+'/usr/share/applications')

    #Copy tag folder to build folder except the windows script
    copytree(tmpDir+folderName,buildDir+'/usr/share/qtodotxt',False,ignore_patterns('qtodotxt.pyw'))
    #Fix execution rights on bin folder
    for file in os.listdir(buildBinDir):
        filePath=os.path.join(buildBinDir,file)
        if os.path.isfile(filePath):
            st = os.stat(filePath)
            os.chmod(filePath, st.st_mode | S_IEXEC)

    # Adding copyright file
    copy(scriptDir+'/copyright',buildDir+'/usr/share/doc/qtodotxt/copyright')
    # Adding desktop file
    copy(scriptDir+'/qtodotxt.desktop',buildDir+'/usr/share/applications/qtodotxt.desktop')
    # Adding changelog file
    f_in = open(scriptDir+'/changelog', 'rb')
    f_out = gzip.open(buildDir+'/usr/share/doc/qtodotxt/changelog.gz', 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()

    return (buildDir,debianDir)


def makeMd5sums(baseDir,outputFilePath):

    excludes = ['DEBIAN','*.pyc']
    excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

    outputFile = open(outputFilePath, 'w')

    for (root,dirs,files) in os.walk(baseDir):
        dirs[:] = [d for d in dirs if not re.match(excludes,d)]
        files = [f for f in files if not re.match(excludes,f)]

        for fn in files:
            path = os.path.join(root,fn)
            md5 = hashlib.md5(open(path,'rb').read()).hexdigest()
            relativePath = root.replace(baseDir+'/',"",1) + os.sep + fn
            outputFile.write("%s %s\n" % (md5,relativePath))
            
    outputFile.close()

def generateControl(templateFile,packageVersion,outputFilePath):
    
    templateExp = open(templateFile,'r').read()
    template = Template(templateExp)

    substitute=template.safe_substitute(version=packageVersion)
    open(outputFilePath,'w').write(substitute)
    #Control file must be owned by root
    os.chown(outputFilePath,0,0)

def buildDeb(version,buildDir):
    # Adding symlink to bin folder
    os.chdir(buildDir+'/usr/bin/')
    os.symlink('../share/qtodotxt/bin/qtodotxt','qtodotxt')

    bashCmd=" ".join(["dpkg -b",buildDir,tmpDir+"qtodotxt_"+version+"_all.deb"])
    call(bashCmd,shell=True)

def clean(fileName,folderName):
    # Removing tar.gz
    os.remove(tmpDir+fileName)
    # Removing untar folder
    rmtree(tmpDir+folderName)
    #Removing build folder
    rmtree(tmpDir+folderName+'_build')


version=sys.argv[1]
scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
# Step 1: download tag from github
fileName = dlTagFromGitHub(version)

# Step 2: uncompress tag's archive
folderName = uncompressFile(fileName)

# Step 3: build Debian package structure
(buildDir,debianDir)=buildPackageFolder(folderName)

# Step 4: build DEBIAN/md5sums file
makeMd5sums(buildDir,debianDir+'md5sums')

# Step 5: generate DEBIAN/control file
generateControl(scriptDir+'/control.tpl',version,debianDir+'control')

# Step 6: build the deb package
buildDeb(version,buildDir)

# Step 7: clean all the mess
clean(fileName,folderName)
