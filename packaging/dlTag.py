import urllib2
import os
import sys
import tarfile

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
    os.remove(tmpDir+fileName)

fileName = dlTagFromGitHub(sys.argv[1])
uncompressFile(fileName)
