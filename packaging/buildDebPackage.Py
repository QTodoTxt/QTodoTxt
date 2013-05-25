import urllib2
import os
import os.path 
import sys
import tarfile
import shutil
import stat
import fnmatch
import re
import hashlib
from string import Template
from subprocess import call


tmpDir="/tmp/"

def dlTagFromGitHub(version):
    remoteFile = urllib2.urlopen('https://github.com/mNantern/QTodoTxt/archive/'+version+'.tar.gz')
    contentDisposition=remoteFile.info()['Content-Disposition']
    fileName=contentDisposition.split('=')[1]

    localFile = open(tmpDir+fileName, 'wb')
    localFile.write(remoteFile.read())
    localFile.close()
    return fileName


def purgeArchive(members):
    for tarinfo in members:
        if os.path.split(tarinfo.name)[1] not in [".gitignore",".gitattributes"]:
            yield tarinfo

def uncompressFile(fileName):
    os.chdir(tmpDir)
    tar = tarfile.open(tmpDir+fileName)
    tar.extractall(members=purgeArchive(tar))
    tar.close()
    return fileName.rsplit(".",2)[0]

def buildPackageFolder(folderName):
    buildDir=tmpDir+folderName+'_build'
    buildBinDir=buildDir+'/usr/share/qtodotxt/bin/'
    debianDir=buildDir+'/DEBIAN/'

    # Tree structure
    os.makedirs(debianDir)
    os.makedirs(buildDir+'/usr/bin/')

    #Copy tag folder to build folder
    shutil.copytree(tmpDir+folderName,buildDir+'/usr/share/qtodotxt')
    #Fix execution rights on bin folder
    for file in os.listdir(buildBinDir):
        filePath=os.path.join(buildBinDir,file)
        if os.path.isfile(filePath):
            st = os.stat(filePath)
            os.chmod(filePath, st.st_mode | os.stat.S_IEXEC)

    # Adding symlink to bin folder
    os.chdir(tmpDir+folderName+'_build'+'/usr/bin/')
    os.symlink('../share/qtodotxt/bin/qtodotxt','qtodotxt')
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
            relativePath = root.replace(baseDir,"",1) + os.sep + fn
            outputFile.write("%s %s\n" % (md5,relativePath))
            
    outputFile.close()

def generateControl(templateFile,packageVersion,outputFilePath):
    
    templateExp = open(templateFile,'r').read()
    template = Template(templateExp)

    substitute=template.safe_substitute(version=packageVersion)
    open(outputFilePath,'w').write(substitute)

def buildDeb(version,buildDir):
    bashCmd=" ".join(["dpkg -b",buildDir,tmpDir+"qtodotxt_"+version+"_all.deb"])
    call(bashCmd,shell=True)

def clean(fileName,folderName):
    # Removing tar.gz
    os.remove(tmpDir+fileName)
    # Removing untar folder
    shutil.rmtree(tmpDir+folderName)
    #Removing build folder
    shutil.rmtree(tmpDir+folderName+'_build')


version=sys.argv[1]

# Step 1: download tag from github
fileName = dlTagFromGitHub(version)

# Step 2: uncompress tag's archive
folderName = uncompressFile(fileName)

# Step 3: build Debian package structure
(buildDir,debianDir)=buildPackageFolder(folderName)

# Step 4: build DEBIAN/md5sums file
makeMd5sums(buildDir,debianDir+'md5sums')

# Step 5: generate DEBIAN/control file
generateControl('Debian/control.tpl',version,debianDir+'control')

# Step 6: build the deb package
buildDeb(version,buildDir)

# Step 7: clean all the mess
clean(fileName,folderName)
