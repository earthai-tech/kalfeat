# -*- coding: utf-8 -*-
#   author-email: <etanoyau@gmail.com>
#   Licence:  GPL-3.0 
"""
 A package for fast detecting the geo-electrical features 
==========================================================

`kalfeat`_ (stands for `Kouadio et al.`_  features detection) is designed for 
predicting the groundwater flow rate from the geology and DC resistivity data
is designed to bring a piece solution in the detection of the geo-electrical 
features which are known as the foremost criteria to select the right location 
before any drilling locations. The aim of kalfeat is twofold::
    1. to minimize the rate of unsuccessful drillings after the geological 
        survey during CDWS and save money from geophysical and drilling companies.
    2. to maximize the number of boreholes intended for the populations and 
    encourage the partners to indirectly solve the problem of water scarcity. 
    
.. _Kouadio et al. : https://doi.org/10.1029/2021wr031623
.. _kalfeat: https://github.com/WEgeophysics/kalfeat/

"""
import os 
import sys 

__version__='0.1.0'
__author__='Kouadio Laurent' 

from . import (  
    _kalfeatlog, 
    methods, 
    tools,
    decorators, 
    documentation, 
    exceptions, 
    property, 
    sklearn,
    typing, 
    __main__, 
    
    )

if __name__ =='__main__' or __package__ is None: 
    sys.path.append( os.path.dirname(os.path.dirname(__file__)))
    sys.path.insert(0, os.path.dirname(__file__))
    __package__ ='kalfeat'


