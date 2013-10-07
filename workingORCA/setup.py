#from distutils.core import setup
#import py2exe
#import matplotlib
#setup(
#    data_files=matplotlib.get_py2exe_datafiles(),
#    console=['ORCAGUI.py'])
#
from distutils.core import setup
import py2exe
from distutils.filelist import findall
import os
import matplotlib
matplotlibdatadir = matplotlib.get_data_path()
matplotlibdata = findall(matplotlibdatadir)
matplotlibdata_files = []
for f in matplotlibdata:
    dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
    matplotlibdata_files.append((os.path.split(dirname)[0], [f]))
setup(
       windows=['ORCAGUI.py'],
       options={
                'py2exe': {
                           'packages' : ['matplotlib'],
                           "dll_excludes": ["MSVCP90.dll"],
                           #'includes' : ['backend_tkagg'],
                          }
               },
       data_files=matplotlibdata_files
     )
