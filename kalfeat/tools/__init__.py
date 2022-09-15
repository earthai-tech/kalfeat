# -*- coding: utf-8 -*-

import os
import  re
import numpy as np

from .coreutils import ( 
    plotAnomaly, 
    vesSelector, 
    erpSelector, 
    defineConductiveZone, 
    )
from .exmath import ( 
    type_,
    shape, 
    power, 
    magnitude, 
    sfi, 
    ohmicArea, 
    invertVES, 
    vesDataOperator, 
    scalePosition,
    )
from ..decorators import gdal_data_check

HAS_GDAL = gdal_data_check(None)._gdal_data_found
NEW_GDAL = False

if (not HAS_GDAL):
    try:
        import pyproj
    except ImportError:
        raise RuntimeError("Either GDAL or PyProj must be installed")
else:
    import osgeo
    if hasattr(osgeo, '__version__') and int(osgeo.__version__[0]) >= 3:
        NEW_GDAL = True


