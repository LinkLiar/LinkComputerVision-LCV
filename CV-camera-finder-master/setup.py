__author__ = 'Lika'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize


sourcefiles = ['CameraFinder.cpp', 'cap.cpp']

ext_modules = [
    # cythonize("CameraFinder.cpp")
    # V2 Beta
    Extension("CameraFinder", sourcefiles,
              include_dirs=["capture"],
              # error LNK2001: unresolved external symbol __imp_CoTaskMemFree
              libraries=["ole32"],
              language="c++"),
]
setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(
        ext_modules,
        compiler_directives={'language_level': "3"}),
)
