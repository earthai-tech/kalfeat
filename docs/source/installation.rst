Installation
============

Installing via pip 
------------------
To install the `kalfeat` package from the Python package index into an established
Python environment, use the pip command:

.. code-block:: bash
   
   pip install kalfeat 
   

Intalling from source 
----------------------
To install from source, clone the project with git: 

.. code-block:: bash 

   git clone https://github.com/WEgeophysics/kalfeat.git 
  
Or download the latest version from the project webpage: https://github.com/WEgeophysics/kalfeat

In the source directory use the command

.. code-block:: bash

   python setup.py install
   
   
Required Dependencies
---------------------
`pycsamt` was originally built on python 3.6. However, the last version requires at least **python 3.8**.

It calls on the core Python data analytics stack, and a third party parsing library:

* numpy
* scipy
* Pandas
* xlrd
* regex
* tqdm
* pytest
* pyyaml
* qtpy

These modules should build automatically if you are installing via `pip`. If you are building from
the source code, or if pip fails to load them, they can be loaded with the same `pip` syntax as
above.   



