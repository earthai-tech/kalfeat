# -*- coding: utf-8 -*-
"""
 Test utilities 
 ^^^^^^^^^^^^^^

"""
import os
# import datetime
import  unittest 
import pytest
import numpy as np 
import pandas as pd 

from tests import ( 
    ERP_DATA_DIR,
    TEST_TEMP_DIR, 
    DATA_UNSAFE_XLS, 
    DATA_UNSAFE, 
    DATA_SAFE, 
    DATA_SAFE_XLS,
    DATA_EXTRA ,
    PREFIX
)
from tests.utilities.__init__ import (
    dipoleLength, 
    dipoleLengthX, 
    array1D , 
    array2D, 
    array2DX, 
    extraarray2D, 
)
from tests import make_temp_dir
from tests.methods.__init__ import (reset_matplotlib,
                                 kalfeatlog, 
                                 diff_files)
from kalfeat.tools.coreutils import erpSelector

from kalfeat.tools.exmath import (
    power ,
    magnitude , 
    _find_cz_bound_indexes
                                
) 
class TestUtils(unittest.TestCase):
    """
    Test electrical resistivity profile  and compute geo-lectrical features 
    as followings : 
        - type 
        - shape 
        - sfi 
        - power 
        - magnitude
        - anr
        - select_best_point
        - select_best_value
    """
    data_collections = ( DATA_UNSAFE_XLS, DATA_UNSAFE, DATA_SAFE,
                        DATA_SAFE_XLS, DATA_EXTRA, 
        array1D , array2D, array2D [:, :2],  array2DX, extraarray2D
        
        )

    @classmethod 
    def setUpClass(cls):
        """
        Reset building matplotlib plot and generate tempdir inputfiles 
        
        """
        reset_matplotlib()
        cls._temp_dir = make_temp_dir(cls.__name__)

    def setUp(self): 
        if not os.path.isdir(TEST_TEMP_DIR):
            print('--> outdir not exist , set to None !')
            kalfeatlog.get_kalfeat_logger().error('Outdir does not exist !')
            
    def test_find_cz_bound_indexes (self): 
        
        pass 
    def test_assert_station_positions (self): 
        pass 
    
    def test_sanitize_collected_data (self) :
        """ Test the capability of the  func to  read and fetch data 
        straigthly from `csv` and `xlsx` and sanitize data to fit the 
        corresponding ``PREFIX``. """

        for i, f in enumerate(self.data_collections):
            print('i=', i)
            df =  erpSelector( f)
            col = list(df.columns) if isinstance(df, pd.DataFrame) else [df.name] # for Series
            if os.path.isfile (f): 
                print(os.path.basename(os.path.splitext(f)[0].lower()) )
                if os.path.basename(os.path.splitext(f)[0].lower()) in (
                        'testunsafedata', 'testunsafedata_extra'): 
                    print('PASSED')
                    print('col ==', col)
                    self.assertListEqual(col , ['station', 'resistivity',
                                                'longitude', 'latitude',
                                                'easting', 'northing'])
                    
                elif os.path.basename(os.path.splitext(f)[0].lower()) =='testsafedata': 
                    self.assertEqual(len(col), len(PREFIX ),
                        f'The length of data columns={col}  is '
                        f' different from the expected length ={len(PREFIX)}.')
   
            elif isinstance(f, pd.Series): 
                self.assertListEqual (col , ['resistivity'], 
                                     'Expected a sery of "resistivity" by got'
                                     f'{f.name}')
            elif isinstance(f, pd.DataFrame): 
                self.assertListEqual (col , ['station', 'resistivity'], 
                        'Expected a sery of "[station , resistivity]" by got'
                        f'{col}')
                
if __name__=='__main__': 
    unittest.main()

    












































