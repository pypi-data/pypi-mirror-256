# Autopysta
Autopysta is a Python library for modeling 2D traffic on highways. It is written natively in C++ for better perfomance and wrapped by SWIG for use on Python.

## Important
If the installation is on Windows you have to keep in mind that the Python version has to be 3.8. Otherwise it will install but not work properly due to probelms with the dll. 

Linux doesn't have this problem and works for 3.8 onwards.

## Details
The package comes with a .so (for Linux systems) and a .pyd (for Windows) and a .py that use those files depending on the platform.

Currently there is no support for Mac OS for it is planned for the future.

## How to use it
To use autopysta you just have to import it in Python:

    import autopysta

Then it can be used to make simulations with vehicles that move and change tracks according to the models chosen in a highway defined by the user. We are working on a documentation to explain how to use all of it.

 


