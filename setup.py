from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension

# Define the extension module
ext_modules = [
    Extension(
        name="BP",  # This is the name of the compiled extension module (BP.so or BP.pyd)
        sources=["Bp.pyx"],  # List of source files (here, just BP.pyx)
        language="c++",  # Specify C++ because you're using C++ code
        extra_compile_args=["-std=c++11"],  # If you're using C++11 features
    )
]

# Set up the package and build the extension
setup(
    name="BP",  # Name of your package/module
    ext_modules=cythonize(ext_modules),  # Use cythonize to compile the extension
    zip_safe=False,  # Recommended for compiled extensions
)