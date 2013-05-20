import os

os.system('coverage run run-tests.py')
os.system('coverage html -d .testOutput/html')
os.system(os.path.join('.testOutput', 'html', 'index.html'))