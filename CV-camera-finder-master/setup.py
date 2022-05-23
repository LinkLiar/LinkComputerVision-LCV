from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

sourcefiles = ['CameraFinder.cpp', 'capture.cpp']

ext_modules = [
    Extension("CameraFinder", sourcefiles,
              libraries=["ole32"],
              language="c++"),
]    # cythonize("CameraFinder.cpp")
setup(
    name='CameraFinder',
    version='1.0',
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(
        ext_modules,
        compiler_directives={'language_level': "3"}),
)
