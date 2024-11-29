from setuptools import setup, Extension
import pybind11

setup(
    name="blood_pressure",
    ext_modules=[
        Extension(
            "blood_pressure",  # This is the name of the Python module
            ["blood_pressure_monitoring.cpp"],  # Add all your source files here
            include_dirs=[pybind11.get_include()],  # Pybind11 headers
            language="c++",
            extra_compile_args=["-std=c++11"]  # Ensure C++11 is used
        )
    ],
)