import os

for dirName, subdirList, fileList in os.walk('.'):
    path = os.path.join(dirName, '__init__.py')
    
    if not os.path.exists(path):
        print 'Creating %s...' % path
        open(path, 'w').flush()

    for file in fileList:
        path = os.path.join(dirName, file)
        
        if path.endswith('pyc_dis'):
            print 'Renaming %s' % path
            os.rename(path, path[:-5])
        
        if path.endswith('pyc'):
            print 'Removing %s' % path
            os.remove(path)