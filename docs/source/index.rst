.. kalfeat documentation master file, created by
   sphinx-quickstart on Sun Feb 28 23:20:06 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`kalfeat` documentation
===========================

Why `kalfeat` ? 
^^^^^^^^^^^^^^^

`kalfeat` (stands for `Kouadio et al. <https://doi.org/10.1029/2021wr031623>`_ features detection) is designed
for predicting the groundwater flow rate (FR) from the geology and DC resistivity data. In developing countries, 
during the campaigns for drinking water supply (CDWS), the DC-resistivity method is mostly used especially 
the electrical resistivity profiling (ERP) for detecting the conductive zone and the vertical Electrical 
sounding (VES) to speculate about the existence of the fracture zone before proposing a drilling point. 
However, despite the use of both methods, the accurate drilling point after ERP and VES was not always the best and 
faced some difficulties. To workaround this problem, some geological companies try to propose at least three 
points to maximize their chance to get the FR required (FRR) by the project depending on 
the number of living population in the survey area. This trick has three shortcomings:
 
* first, one unsuccessful borehole costs at around 25 245 $US and 8 415$US per survey, which is an expensive loss especially when the CDWS covers at least 2000 villages. 
* second, if all three proposed points fail to give the RFR, the local companies must take the whole fees in charge  to make a new survey. This occasionally creates a loss of investments from partners and governments. 
* the last issue is the numerous of unsustainable boreholes obtained after a few year of use by the population. Indeed, the borehole becomes unsustainable when it dried up after a few years of use. This is a critial issue frequently occurs when the FR is sufficiently not enough to satisfy the living population demand. Although, the climate change is one 
 of the cause of that issue, the other factor is caused by  the use of the traditional criteria (criteria mostly used by geophysicists to speculate about the 
 goodness of the proposed drilling point) for determining the expected drilling points using ERP and VES. 

Benefits of `kalfeat` 
^^^^^^^^^^^^^^^^^^^^^^^^

Faced with the problems enumerated above, `kalfeat` is designed to bring a piece solution in the detection of the geo-electrical features which are known as 
the foremost criteria to select the right location before any drilling locations. The aim of `kalfeat` is twofold:

1. minimize the rate of unsuccessful drillings after the geological survey during CDWS and save money from geophysical and drilling companies. 
2. maximize the number of boreholes intended for the populations and also encourage the partners to indirectly solve the problem of water scarcity. 

One can read the paper below to better understand the `kalfeat` features definitions:: 

      Kouadio, K. L., Kouame, L. N., Drissa, C., Mi, B., Kouamelan, K. S., Gnoleba, S. P. D., et al. (2022). Groundwater Flow Rate Prediction from Geo‐Electrical Features using Support Vector Machines. Water Resources Research, (May 2022). https://doi.org/10.1029/2021wr031623*
    

`kalfeat` API 
^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   installation
   api


Indices and tables
====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
