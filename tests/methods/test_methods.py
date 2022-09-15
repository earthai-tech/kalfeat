# -*- coding: utf-8 -*-


"""
Test module methods 

"""
import os
import numpy as np 
# import datetime
import  unittest 
import pytest
from kalfeat.methods import (
    ResistivityProfiling, 
    VerticalSounding 
    )
from tests import ( 
    DATA_UNSAFE, 
    TEST_TEMP_DIR, 
    make_temp_dir ,
    DATA_VES 
    ) 
from tests.methods.__init__ import reset_matplotlib, kalfeatlog, diff_files

class TestERP(unittest.TestCase):
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
    dipole_length = 10. 

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
        
    @pytest.mark.skip(reason='Test succeeded on Windox env. With Python 3.7'
                      'but required latest version of pandas library on '
                      'Linux env.')  
    def fit_erp(self):
        """
        Test geo-electricals features computations from ERP 

        Examples
        --------
        >>> from kalfeat.methods.electrical import ResistivityProfiling 
        >>> rObj = ResistivityProfiling(AB= 200, MN= 20,station ='S7') 
        >>> rObj.fit('data/erp/testunsafedata.csv')
        >>> rObj.sfi_
        ... array([0.03592814])
        >>> rObj.power_, robj.position_zone_
        ... 90, array([ 0, 30, 60, 90])
        >>> rObj.magnitude_, rObj.conductive_zone_
        ... 268, array([1101, 1147, 1345, 1369], dtype=int64)
        >>> rObj.dipole
        ... 30
            
        """
        
        rObj = ResistivityProfiling(AB= 200, MN= 20,station ='S7') 
        rObj.fit(DATA_UNSAFE)
        self.assertAlmostEqual(rObj.sfi_, .03) 
        self.assertIsInstance(rObj.power_, float) 
        self.assertIsInstance(rObj.position_zone_, np.ndarray)
        self.assertIsInstance(rObj.magnitude_, float) 
        self.assertAlmostEqual(rObj.magnitude_, 268) 
        self.assertIsInstance(rObj.conductive_zone_, np.ndarray)
        self.assertAlmostEqual(rObj.dipole, 30) 

    def fit_ves(self):
        """
        Test geo-electricals features computations from VES
        Examples
        -------- 
        >>> from kalfeat.methods import VerticalSounding 
        >>> from kalfeat.tools import vesSelector 
        >>> vobj = VerticalSounding(fromS= 45, vesorder= 3)
        >>> vobj.fit('data/ves/ves_gbalo.xlsx')
        >>> vobj.ohmic_area_ # in ohm.m^2
        ... 349.6432550517697
        >>> vobj.nareas_ # number of areas computed 
        ... 2
        >>> vobj.area1_, vobj.area2_ # value of each area in ohm.m^2 
        ... (254.28891096053943, 95.35434409123027) 
        >>> vobj.roots_ # different boundaries in pairs 
        ... [array([45.        , 57.55255255]), array([ 96.91691692, 100.  ])]
        >>> data = vesSelector ('data/ves/ves_gbalo.csv', index_rhoa=3)
        >>> vobj = VerticalSounding().fit(data)
        >>> vobj.fractured_zone_ # AB/2 position from 45 to 100 m depth.
        ... array([ 45.,  50.,  55.,  60.,  70.,  80.,  90., 100.])
        >>> vobj.fractured_zone_resistivity_
        ...array([57.67588974, 61.21142365, 64.74695755, 68.28249146, 75.35355927,
               82.42462708, 89.4956949 , 96.56676271])
        >>> vobj.nareas_ 
        ... 2
        >>> vobj.ohmic_area_
        ... 349.6432550517697

        """
        vobj = VerticalSounding(fromS= 45, vesorder= 3)
        vobj.fit(DATA_VES)
        
        self.assertAlmostEqual(vobj.area1_, 349.) 
        self.assertAlmostEqual(vobj.area2_, 95.) 
        self.assertIsInstance(vobj.roots_, np.ndarray)  
        self.assertIsInstance(vobj.fractured_zone_, np.ndarray)
        self.assertIsInstance(vobj.fractured_zone_resistivity_, np.ndarray)
        self.assertAlmostEqual(vobj.nareas_ , 2) 
        
def compare_diff_files(refout, refexp):
    """
    Compare diff files like expected files and output files generated after 
    runnning scripts.
    
    :param refout: 
        
        list of reference output files generated after runing scripts
        
    :type refout: list 
    
    :param refexp: recreated expected files for comparison 
    :param refexp: list 

    """
    for outfile , expfile in zip(sorted(refout), 
                                   sorted(refexp)):
            unittest.TestCase.assertTrue(os.path.isfile(outfile),
                                "Ref output data file does not exist,"
                                "nothing to compare with"
                                )
            
            print(("Comparing", outfile, "and", expfile))
            
            is_identical, msg = diff_files(outfile, expfile, ignores=['Date/Time:'])
            print(msg)
            unittest.TestCase.assertTrue(is_identical, 
                            "The output file is not the same with the baseline file.")
    


if __name__=='__main__':

    unittest.main()
    
    
                
    
    
    
    
    
    
    
    
    
    
    