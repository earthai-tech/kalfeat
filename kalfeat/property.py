# -*- coding: utf-8 -*-
#   author: KLaurent <etanoyau@gmail.com>
#   Licence:  GPL-3.0 
 

"""
`kalfeat`_ property 
=====================

**Water**: Base class module. It contains all the water properties usefull 
    for pure hydrogeological module writting. Instanciated the class should 
    raise an error, however, its special attributes can be used by the child 
    class object. 
    
**BasePlot**: The base class of all plots. It can be the parent class of all 
    other plotting classes. The module :mod:`~.view.plot` uses the `BasePlot`
    class for `Matplotlib plot`_.
    
**P**: Is a property class that handles the |ERP| and |VES| attributes. Along 
    the :mod:`~.methods.electrical`, it deals with the electrical dipole 
    arrangements, the data classsification and assert whether it is able to 
    be read by the scripts. It is a lind of "asserter". Accept data or reject 
    data provided by the used indicated the way to sanitize it before feeding 
    to the algorithm:: 
        
        >>> from kalfeat.property import P 
        >>> pObj = P() 
        >>> P.idictags 
        ... <property at 0x15b2248a450>
        >>> pObj.idicttags 
        ... {'station': ['pk', 'sta', 'pos'],
        ...     'resistivity': ['rho', 'app', 'res', 'se', 'sounding.values'],
        ...     'longitude': ['long', 'lon'],
        ...     'latitude': ['lat'],
        ...     'easting': ['east', 'x'],
        ...     'northing': ['north', 'y']}
        >>> rphead = ['res', 'x', 'y', '']
        >>> pObj (rphead) # sanitize the given resistivity profiling head data.
        ... ['resistivity', 'easting', 'northing']
        >>> rphead = ['lat', 'x', 'rho', '']
        ... ['latitude', 'easting', 'resistivity']
        >>> rphead= ['pos', 'x', 'lon', 'north', 'latitud', 'app.res' ]
        >>> pObj (rphead)
        ... ['station', 'easting', 'longitude', 'northing', 'latitude', 'resistivity'] 
        >>> # --> for sounding head assertion 
        >>> vshead=['ab', 's', 'rho', 'potential']
        >>> pObj (vshead, kind ='ves')
        ... ['AB', 'resistivity'] # in the list of vshead, 
        ... # only 'AB' and 'resistivity' columns are recognized. 
            
**ElectricalMethods**: Is another Base class of :mod:`~.methods.dc` 
    especially the :class:`~.methods.dc.ResistivityProfiling` and 
    :class:`~.methods.electrical.VerticalSounding`. It is composed of the 
    details of geolocalisation of the survey area and the array configuration. 
    It expects to hold other attributes as the development is still ongoing.
   
.. _kalfeat: https://github.com/WEgeophysics/kalfeat/
.. |ERP| replace:: Electrical resistivity profiling 
.. |VES| replace:: Vertical Electrical Sounding 

"""
# import warnings 
from __future__ import annotations 

from abc import ( 
    ABC, 
    abstractmethod, 
    )

from .decorators import refAppender 
from .documentation import __doc__ 



__all__ = [ 
    "Water",
    'P',
    "ElectricalMethods", 
    "assert_arrangement"
]

array_configuration ={
    1 : (
        ['Schlumberger','AB>> MN','slbg'], 
        'S'
        ), 
    2 : (
        ['Wenner','AB=MN'], 
         'W'
         ), 
    3: (
        ['Dipole-dipole','dd','AB<BM>MN','MN<NA>AB'],
        'DD'
        ), 
    4: (
        ['Gradient-rectangular','[AB]MN', 'MN[AB]','[AB]'],
        'GR'
        )
    }

  
utm_zone_designator ={
    'X':[72,84], 
    'W':[64,72], 
    'V':[56,64],
    'U':[48,56],
    'T':[40,48],
    'S':[32,40], 
    'R':[24,32], 
    'Q':[16,24], 
    'P':[8,16],
    'N':[0,8], 
    'M':[-8,0],
    'L':[-16, 8], 
    'K':[-24,-16],
    'J':[-32,-24],
    'H':[-40,-32],
    'G':[-48,-40], 
    'F':[-56,-48],
    'E':[-64, -56],
    'D':[-72,-64], 
    'C':[-80,-72],
    'Z':[-80,84]
}
    

@refAppender(__doc__) 
class Water (ABC): 
    r""" Should be a SuperClass for methods classes which deals with water 
    properties and components. Instanciate the class shoud raise an error. 
    
    Water (H2O) is a polar inorganic compound that is at room temperature a 
    tasteless and odorless liquid, which is nearly colorless apart from an 
    inherent hint of blue. It is by far the most studied chemical compound 
    and is described as the "universal solvent"and the "solvent of life".
    It is the most abundant substance on the surface of Earth and the only 
    common substance to exist as a solid, liquid, and gas on Earth's surface.
    It is also the third most abundant molecule in the universe 
    (behind molecular hydrogen and carbon monoxide).
    
    The Base class initialize arguments for different methods such as the 
    |ERP| and for |VES|. The `Water` should set the attributes and check 
    whether attributes are suitable for what the specific class expects to. 
    
    Hold some properties informations: 
        
    =================   =======================================================
    Property            Description        
    =================   =======================================================
    state               official names for the chemical compound r"$H_2O$". It 
                        can be a matter of ``solid``, ``ice``, ``gaseous``, 
                        ``water vapor`` or ``steam``. The *default* is ``None``.
    taste               water from ordinary sources, including bottled mineral 
                        water, usually has many dissolved substances, that may
                        give it varying tastes and odors. Humans and other 
                        animals have developed senses that enable them to
                        evaluate the potability of water in order to avoid 
                        water that is too ``salty`` or ``putrid``. 
                        The *default* is ``potable``.    
    odor                Pure water is usually described as tasteless and odorless, 
                        although humans have specific sensors that can feel 
                        the presence of water in their mouths,and frogs are known
                        to be able to smell it. The *default* is ``pure``.
    color               The color can be easily observed in a glass of tap-water
                        placed against a pure white background, in daylight.
                        The **default** is ``pure white background``. 
    appearance          Pure water is visibly blue due to absorption of light 
                        in the region ca. 600 nm – 800 nm. The *default* is 
                        ``visible``. 
    density             Water differs from most liquids in that it becomes
                        less dense as it freezes. In 1 atm pressure, it reaches 
                        its maximum density of ``1.000 kg/m3`` (62.43 lb/cu ft)
                        at 3.98 °C (39.16 °F). The *default* units and values
                        are ``kg/m3``and ``1.`` 
    magnetism           Water is a diamagnetic material. Though interaction
                        is weak, with superconducting magnets it can attain a 
                        notable interaction. the *default* value is 
                        :math:`-0.91 \chi m`". Note that the  magnetism  
                        succeptibily has no unit. 
    capacity            stands for `heat capacity`. In thermodynamics, the 
                        specific heat capacity (symbol cp) of a substance is the
                        heat capacity of a sample of the substance divided by 
                        the mass of the sample. Water has a very high specific
                        heat capacity of 4184 J/(kg·K) at 20 °C 
                        (4182 J/(kg·K) at 25 °C).The *default* is is ``4182 ``
    vaporization        stands for `heat of vaporization`. Indeed, the enthalpy  
                        of vaporization (symbol :math:`\delta H_{vap}`), also  
                        known as the (latent) heat of vaporization or heat of 
                        evaporation, is the amount of energy (enthalpy) that  
                        must be added to a liquid substance to transform a 
                        quantity of that substance into a gas. Water has a high 
                        heat of vaporization i.e. 40.65 kJ/mol or 2257 kJ/kg 
                        at the normal boiling point), both of which are a  
                        result of the extensive hydrogen bonding between its 
                        molecules. The *default* is ``2257 kJ/kg``. 
    fusion              stands for `enthalpy of fusion` more commonly known as 
                        latent heat of water is 333.55 kJ/kg at 0 °C. The 
                        *default* is ``33.55``.
    miscibility         Water is miscible with many liquids, including ethanol
                        in all proportions. Water and most oils are immiscible 
                        usually forming layers according to increasing density
                        from the top. *default* is ``True``.                    
    condensation        As a gas, water vapor is completely miscible with air so 
                        the vapor's partial pressure is 2% of atmospheric 
                        pressure and the air is cooled from 25 °C, starting at
                        about 22 °C, water will start to condense, defining the
                        dew point, and creating fog or dew. The *default* is the 
                        degree of condensation set to ``22°C``. 
    pressure            stands for `vapour pressure` of water. It is the pressure 
                        exerted by molecules of water vapor in gaseous form 
                        i.e. whether pure or in a mixture with other gases such
                        as air.  The vapor pressure is given as a list from the 
                        temperature T, 0°C (0.6113kPa) to 100°C(101.3200kPa). 
                        *default* is ``(0.611, ..., 101.32)``.
    compressibility     The compressibility of water is a function of pressure 
                        and temperature. At 0 °C, at the limit of zero pressure,
                        the compressibility is ``5.1x10^−10 P^{a^−1}``. 
                        The *default* value is the value at 0 °C.
    triple              stands for `triple point`. The temperature and pressure
                        at which ordinary solid, liquid, and gaseous water 
                        coexist in equilibrium is a triple point of water. The 
                        `triple point` are set to (.001°C,611.657 Pa) and 
                        (100 , 101.325kPa) for feezing (0°C) and boiling point
                        (100°C) points. In addition, the `triple point` can be
                        set as ``(20. , 101.325 kPa)`` for 20°C. By *default*,
                        the `triple point` solid/liquid/vapour is set to 
                        ``(.001, 611.657 Pa )``.
    melting             stands for `melting point`. Water can remain in a fluid
                        state down to its homogeneous nucleation point of about
                        231 K (−42 °C; −44 °F). The melting point of ordinary
                        hexagonal ice falls slightly under moderately high 
                        pressures, by 0.0073 °C (0.0131 °F)/atm[h] or about 
                        ``0.5 °C`` (0.90 °F)/70 atm considered as the 
                        *default* value.                   
    conductivity        In pure water, sensitive equipment can detect a very 
                        slight electrical conductivity of 0.05501 ± 0.0001 
                        μS/cm at 25.00 °C. *default* is  ``.05501``.  
    polarity            An important feature of water is its polar nature. The
                        structure has a bent molecular geometry for the two 
                        hydrogens from the oxygen vertex. The *default* is 
                        ``bent molecular geometry`` or ``angular or V-shaped``. 
                        Other possibility is ``covalent bonds `` 
                        ``VSEPR theory`` for Valence Shell Electron Repulsion.
    cohesion            stands for the collective action of hydrogen bonds 
                        between water molecules. The *default* is ``coherent``
                        for the water molecules staying close to each other. 
                        In addition, the `cohesion` refers to the tendency of
                        similar or identical particles/surfaces to cling to
                        one another.
    adhesion            stands for the tendency of dissimilar particles or 
                        surfaces to cling to one another. It can be 
                        ``chemical adhesion``, ``dispersive adhesion``, 
                        ``diffusive adhesion`` and ``disambiguation``.
                        The *default* is ``disambiguation``.
    tension             stands for the tendency of liquid surfaces at rest to 
                        shrink into the minimum surface area possible. Water 
                        has an unusually high surface tension of 71.99 mN/m 
                        at 25 °C[63] which is caused by the strength of the
                        hydrogen bonding between water molecules. This allows
                        insects to walk on water. The *default*  value is to 
                        ``71.99 mN/m at 25 °C``. 
    action              stands for `Capillary action`. Water has strong cohesive
                        and adhesive forces, it exhibits capillary action. 
                        Strong cohesion from hydrogen bonding and adhesion 
                        allows trees to transport water more than 100 m upward.
                        So the *default* value is set to ``100.``meters. 
    issolvent           Water is an excellent solvent due to its high dielectric
                        constant. Substances that mix well and dissolve in water
                        are known as hydrophilic ("water-loving") substances,
                        while those that do not mix well with water are known
                        as hydrophobic ("water-fearing") substances.           
    tunnelling          stands for `quantum tunneling`. It is a quantum 
                        mechanical phenomenon whereby a wavefunction can 
                        propagate through a potential barrier. It can be 
                        ``monomers`` for the motions which destroy and 
                        regenerate the weak hydrogen bond by internal rotations, 
                        or ``hexamer`` involving the concerted breaking of two 
                        hydrogen bond. The *default* is ``hexamer`` discovered 
                        on 18 March 2016.
    reaction            stands for `acide-base reactions`. Water is 
                        ``amphoteric`` i.e. it has the ability to act as either
                        an acid or a base in chemical reactions.
    ionization          In liquid water there is some self-ionization giving 
                        ``hydronium`` ions and ``hydroxide`` ions. *default* is 
                        ``hydroxide``. 
    earthmass           stands for the earth mass ration in "ppm" unit. Water 
                        is the most abundant substance on Earth and also the 
                        third most abundant molecule in the universe after the 
                        :math:`H_2 \quad \text{and} \quad CO` . The *default* 
                        value is ``0.23``ppm of the earth's mass. 
    occurence           stands for the abundant molecule in the Earth. Water 
                        represents ``97.39%`` of the global water volume of
                        1.38×109 km3 is found in the oceans considered as the 
                        *default* value.
    pH                  stands for `Potential of Hydrogens`. It also shows the 
                        acidity in nature of water. For instance the "rain" is
                        generally mildly acidic, with a pH between 5.2 and 5.8 
                        if not having any acid stronger than carbon dioxide. At
                        neutral pH, the concentration of the hydroxide ion 
                        (:math:`OH^{-}`) equals that of the (solvated) hydrogen 
                        ion(:math:`H^{+}`), with a value close to ``10^−7 mol L^−1`` 
                        at 25 °C. The *default* is ``7.`` or ``neutral`` or the
                        name of any substance `pH` close to.
    nommenclature       The accepted IUPAC name of water is ``oxidane`` or 
                        simply ``water``. ``Oxidane`` is only intended to be 
                        used as the name of the mononuclear parent hydride used
                        for naming derivatives of water by substituent 
                        nomenclature. The *default* name is ``oxidane``.                    
    =================   =======================================================                        
    
    
    See also 
    ----------
    Water (chemical formula H2O) is an inorganic, transparent, tasteless, 
    odorless, and nearly colorless chemical substance, which is the main 
    constituent of Earth's hydrosphere and the fluids of all known living 
    organisms (in which it acts as a solvent). It is vital for all known 
    forms of life, even though it provides neither food, energy, nor organic 
    micronutrients. Its chemical formula, H2O, indicates that each of its 
    molecules contains one oxygen and two hydrogen atoms, connected by covalent
    bonds. The hydrogen atoms are attached to the oxygen atom at an angle of
    104.45°. "Water" is the name of the liquid state of H2O at standard 
    temperature and pressure.

    """
    
    @abstractmethod 
    def __init__(self, 
                 state: str = None, 
                 taste: str  = 'potable', 
                 odor: int | str = 'pure', 
                 appearance: str = 'visible',
                 color: str = 'pure white background', 
                 capacity: float = 4184. , 
                 vaporization: float  = 2257.,  
                 fusion: float = 33.55, 
                 density: float = 1. ,
                 magnetism: float = -.91, 
                 miscibility: bool  =True , 
                 condensation: float = 22, 
                 pressure: tuple = (.6113, ..., 101.32), 
                 compressibility: float  =5.1e-10, 
                 triple: tuple = (.001, 611.657 ),
                 conductivity: float = .05501,
                 melting: float = .5,       
                 polarity: str  ='bent molecular geometry ', 
                 cohesion: str = 'coherent', 
                 adhesion: str  ='disambiguation', 
                 tension: float  = 71.99, 
                 action: float  = 1.e2 ,
                 issolvent: bool =True, 
                 reaction:str  = 'amphoteric', # 
                 ionisation:str  = "hydroxide", 
                 tunneling: str  = 'hexamer' ,
                 nommenclature: str ='oxidane', 
                 earthmass: float =.23 , 
                 occurence: float = .9739,
                 pH: float| str = 7., 
                 ): 
       
        self.state=state 
        self.taste=taste 
        self.odor=odor
        self.appearance=appearance
        self.color=color
        self.capacity=capacity 
        self.vaporization=vaporization   
        self.fusion=fusion 
        self.density=density  
        self.magnetism=magnetism 
        self.miscibility=miscibility 
        self.condensation=condensation 
        self.pressure=pressure, 
        self.compressibility=compressibility 
        self.triple=triple 
        self.conductivity=conductivity
        self.melting=melting      
        self.polarity=polarity  
        self.cohesion=cohesion 
        self.adhesion=adhesion 
        self.tension=tension 
        self.action=action 
        self.issolvent=issolvent 
        self.reaction=reaction
        self.ionisation=ionisation 
        self.tunneling=tunneling 
        self.nommenclature=nommenclature
        self.earthmass=earthmass 
        self.occurence=occurence 
        self.pH=pH
     
        
class ElectricalMethods (ABC) : 
    """ Base class of geophysical electrical methods 

    The electrical geophysical methods are used to determine the electrical
    resistivity of the earth's subsurface. Thus, electrical methods are 
    employed for those applications in which a knowledge of resistivity 
    or the resistivity distribution will solve or shed light on the problem 
    at hand. The resolution, depth, and areal extent of investigation are 
    functions of the particular electrical method employed. Once resistivity 
    data have been acquired, the resistivity distribution of the subsurface 
    can be interpreted in terms of soil characteristics and/or rock type and 
    geological structure. Resistivity data are usually integrated with other 
    geophysical results and with surface and subsurface geological data to 
    arrive at an interpretation. Get more infos by consulting this
    `link <https://wiki.aapg.org/Electrical_methods>`_ . 
    
    
    The :class:`kalfeat.methods.electrical.ElectricalMethods` compose the base 
    class of all the geophysical methods that images the underground using 
    the resistivity values. 
    
    Holds on others optionals infos in ``kws`` arguments: 
       
    ======================  ==============  ===================================
    Attributes              Type                Description  
    ======================  ==============  ===================================
    AB                      float, array    Distance of the current electrodes
                                            in meters. `A` and `B` are used 
                                            as the first and second current 
                                            electrodes by convention. Note that
                                            `AB` is considered as an array of
                                            depth measurement when using the
                                            vertical electrical sounding |VES|
                                            method i.e. AB/2 half-space. Default
                                            is ``200``meters. 
    MN                      float, array    Distance of the current electrodes 
                                            in meters. `M` and `N` are used as
                                            the first and second potential 
                                            electrodes by convention. Note that
                                            `MN` is considered as an array of
                                            potential electrode spacing when 
                                            using the collecting data using the 
                                            vertical electrical sounding |VES|
                                            method i.e MN/2 halfspace. Default 
                                            is ``20.``meters. 
    arrangement             str             Type of dipoles `AB` and `MN`
                                            arrangememts. Can be *schlumberger*
                                            *Wenner- alpha / wenner beta*,
                                            *Gradient rectangular* or *dipole-
                                            dipole*. Default is *schlumberger*.
    area                    str             The name of the survey location or
                                            the exploration area. 
    fromlog10               bool            Set to ``True`` if the given 
                                            resistivities values are collected 
                                            on base 10 logarithm.
    utm_zone                str             string (##N or ##S). utm zone in 
                                            the form of number and North or South
                                            hemisphere, 10S or 03N. 
    datum                   str             well known datum ex. WGS84, NAD27,
                                            etc.         
    projection              str             projected point in lat and lon in 
                                            Datum `latlon`, as decimal degrees 
                                            or 'UTM'. 
    epsg                    int             epsg number defining projection (see 
                                            http://spatialreference.org/ref/ 
                                            for moreinfo). Overrides utm_zone
                                            if both are provided.                           
    ======================  ==============  ===================================
               
    
    Notes
    -------
    The  `ElectricalMethods` consider the given resistivity values as 
    a normal values and not on base 10 logarithm. So if log10 values 
    are given, set the argument `fromlog10` value to ``True``.
    
    .. |VES| replace:: Vertical Electrical Sounding 
    
    """
    
    @abstractmethod 
    def __init__(self, 
                AB: float = 200. , 
                MN: float = 20.,
                arrangement: str  = 'schlumberger', 
                area : str = None, 
                projection: str ='UTM', 
                datum: str ='WGS84', 
                epsg: int =None, 
                utm_zone: str = None,  
                fromlog10:bool =False, 
                verbose: int = 0, 
                ) -> None:
        
        self.AB=AB 
        self.MN=MN 
        self.arrangememt=assert_arrangement(arrangement) 
        self.utm_zone=utm_zone 
        self.projection=projection 
        self.datum=datum
        self.epsg=epsg 
        self.area=area 
        self.fromlog10=fromlog10 
        self.verbose=verbose 
        
            
class P:
    """
    Data properties are values that are hidden to avoid modifications alongside 
    the packages. Its was used for assertion, comparison etceteara. These are 
    enumerated below into a property objects.

    .. |ERP| replace: Electrical resistivity profiling 
    
    Parameters  
    -----------
    
    **frcolortags**: Stands for flow rate colors tags. Values are  
        '#CED9EF','#9EB3DD', '#3B70F2', '#0A4CEF'.
                    
    **ididctags**: Stands for the list of index set in dictionary which encompasses 
        key and values of all different prefixes.
                
    **isation**: List of prefixes used for indexing the stations in the |ERP|. 

    **ieasting**: List of prefixes used for indexing the easting coordinates array. 

    **inorthing**: List of prefixes used to index the northing coordinates. 
     
    **iresistivity** List of prefix used for indexing the apparent resistivity 
        values in the |ERP| data collected during the survey. 

    **isren**: Is the list of heads columns during the data collections. Any data 
        head |ERP| data provided should be converted into 
        the following arangement:
                    
        +----------+-------------+-----------+-----------+
        |station   | resistivity | easting   | northing  | 
        +----------+-------------+-----------+-----------+
            
   **isrll**: Is the list of heads columns during the data collections. Any data 
        head |ERP| data provided should be converted into 
        the following arangement:
                   
        +----------+-------------+-------------+----------+
        |station   | resistivity | longitude   | latitude | 
        +----------+-------------+-------------+----------+
            
    **P**: Typing class for fectching the properties. 
        
    Examples 
    ---------
    >>> from kalfeat.property import P 
    >>> P.idicttags 
    ... <property at 0x1ec1f2c3ae0>
    >>> P().idictags 
    ... 
    {'station': ['pk', 'sta', 'pos'], 'longitude': ['east', 'x', 'long', 'lon'],
     'latitude': ['north', 'y', 'lat'], 'resistivity': ['rho', 'app', 'res']}
    >>> {k:v for k, v in  P.__dict__.items() if '__' not in k}
    ... {'_station': ['pk', 'sta', 'pos'],
         '_easting': ['east', 'x', 'long'],
         '_northing': ['north', 'y', 'lat'],
         '_resistivity': ['rho', 'app', 'res'],
         'frcolortags': <property at 0x1ec1f2fee00>,
         'idicttags': <property at 0x1ec1f2c3ae0>,
         'istation': <property at 0x1ec1f2c3ea0>,
         'ieasting': <property at 0x1ec1f2c39f0>,
         'inorthing': <property at 0x1ec1f2c3c70>,
         'iresistivity': <property at 0x1ec1f2c3e00>,
         'isenr': <property at 0x1ec1f2c3db0>}
    >>> P().isrll 
    ... ['station','resistivity','longitude','latitude']

    """
    
    station_prefix   = [
        'pk','sta','pos'
    ]
    easting_prefix   =[
        'east','x',
                ]
    northing_prefix = [
        'north','y',
    ]
    lon_prefix   =[
        'long', 'lon'
                ]
    
    lat_prefix = [
        'lat'
    ]
    
    resistivity_prefix = [
        'rho','app','res', 'se', 'sounding.values'
    ]
    erp_headll= [
        'station', 'resistivity',  'longitude','latitude',
    ]
    erp_headen= [
        'station', 'resistivity',  'easting','northing',
    ]
    ves_head =['AB', 'MN', 'rhoa']
    
    param_options = [
        ['bore', 'for'], 
        ['x','east'], 
        ['y', 'north'], 
        ['pow', 'puiss', 'pa'], 
        ['magn', 'amp', 'ma'], 
        ['shape', 'form'], 
        ['type'], 
        ['sfi', 'if'], 
        ['lat'], 
        ['lon'], 
        ['lwi', 'wi'], 
        ['ohms', 'surf'], 
        ['geol'], 
        ['flow', 'deb']
    ]
    param_ids =[
        'id', 
        'east', 
        'north', 
        'power', 
        'magnitude', 
        'shape', 
        'type', 
        'sfi', 
        'lat', 
        'lon', 
        'lwi', 
        'ohmS', 
        'geol', 
        'flow'
    ]
    
    ves_props = dict (_AB= ['ab', 'ab/2', 'current.electrodes',
                            'depth', 'thickness'],
                      _MN=['mn', 'mn/2', 'potential.electrodes', 'mnspacing'],
                      )
    
    all_prefixes = { f'_{k}':v for k, v in zip (
        erp_headll + erp_headen[2:] , [
            station_prefix,
            resistivity_prefix,
            lon_prefix,
            lat_prefix, 
            easting_prefix, 
            northing_prefix,
            northing_prefix, 
        ]
        )}
    all_prefixes = {**all_prefixes , **ves_props} 
    
    def __init__( self, hl =None ) :
        self.hl = hl
        for key , value in self.all_prefixes.items() : 
            self.__setattr__( key , value)
            
    
    def _check_header_item (self, it , kind ='erp'): 
        """ Check whether the item exists in the property dictionnary.
        Use param `kind` to select the type of header that the data must 
        collected: 
            `kind` = ``erp`` -> for Electrical Resistivity Profiling  
            `kind` = ``ves`` - > for Vertical Electrical Sounding 
        """
            
        dict_ = self.idictcpr if kind =='ves' else self.idicttags
        for k, val in dict_.items(): 
            for s in val : 
                if str(it).lower().find(s)>=0: 
                    return k 
        return  
                
    def __call__(self, hl: list = None , kind :str  ='erp'):
        """ Rename the given header to hold the  properties 
        header values. 
        
        Call function could  return ``None`` whether the 
        given header item in `hl` does not match any item in property 
        headers. 
        
        :param hl: list or array, 
            list of the given headers. 
        :param kind: str 
            Type of data fed into the algorithm. Can be ``ves`` for Vertical 
            Electrical Sounding  and  ``erp`` for Electrical Resistivity Profiling . 
            
        :Example: 
            >>> from kalfeat.property import P 
            >>> test_v= ['pos', 'easting', 'north', 'rhoa', 'lat', 'longitud']
            >>> pobj = P(test_v)
            >>> pobj ()
            ... ['station', 'easting', 'northing', 'resistivity',
                 'latitude', 'longitude']
            >>> test_v2 = test_v + ['straa', 'nourmai', 'opirn'] 
            >>> pobj (test_v2)
            ... ['station', 'easting', 'northing', 'resistivity', 
                 'latitude', 'longitude']
        """
        
        v_ =list()
        
        self.hl = hl or self.hl 
        if self.hl is not None: 
            self.hl = [self.hl] if isinstance(self.hl, str ) else self.hl
            if hasattr(self.hl, '__iter__'):
                for item in self.hl : 
                    v_.append( self._check_header_item(item, kind)) 
                v_=list(filter((None).__ne__, v_))
                return None if len (v_) ==0 else v_
            
    @property 
    def frcolortags (self): 
        """ set the dictionnary"""
        return  dict ((f'fr{k}', f'#{v}') for k, v in zip(
                        range(4), ('CED9EF','9EB3DD', '3B70F2', '0A4CEF' )
                        )
        )
    @property 
    def idicttags (self): 
        """ Is the collection of data properties """ 
        return  dict ( (k, v) for k, v in zip(
            self.isrll + self.isren[2:],
              [self.istation, self.iresistivity, self.ilon, 
                self.ilat, self.ieasting, self.inorthing ])
                      )
    @property 
    def istation(self) : 
        """ Use prefix to identify station location positions """
        return self._station 
    
    @property 
    def ilon (self): 
        """ Use prefix to identify longitude coordinates if given in the
        dataset. """
        return self._longitude 
    
    @property 
    def ilat(self): 
        """ Use prefix to identify latitude coordinates if given in the
        dataset. """
        return self._latitude
    @property 
    def ieasting  (self): 
        """ Use prefix to identify easting coordinates if given in the
        dataset. """
        return self._easting 
    
    @property 
    def inorthing(self): 
        """ Use prefix to identify northing coordinates if given in the
        dataset. """
        return self._northing
    
    @property 
    def iresistivity(self): 
        """ Use prefix to identify the resistivity values in the dataset"""
        return self._resistivity 
    
    @property 
    def isrll(self): 
        """ `SRLL` is the abbreviation of `S`for ``Stations``,`R`` for 
        resistivity, `L` for ``Longitude`` and `L` for ``Latitude``. 
        `SRLL` is the expected columns in Electrical resistivity profiling.
        Indeed, it keeps the traditional collections sheets
        during the survey. """
        return self.erp_headll
    
    @property 
    def isren(self): 
        """ `SREN` is the abbreviation of `S`for ``Stations``,`R``for 
        resistivity, `E` for ``easting`` and `N` for ``northing``. 
        `SREN` is the expected columns in Electrical resistivity profiling.
        Indeed, it keeps the traditional collections sheets
        during the survey. """
        return self.erp_headen
    @property 
    def icpr (self): 
        """ Keep only the Vertical Electrical Sounding header data ..."""
        return [k.replace('_', '') 
                for k in self.ves_props.keys() ] +['resistivity']
    
    @property 
    def idictcpr (self): 
        """ cpr stands for current-potentials and resistivity. They compose the
        main property values when collected the vertical electrical sounding 
        data."""
        return {f'{k.replace("_", "")}': v  for k , v in {
            **self.ves_props, **{'resistivity': self.iresistivity}}.items()}
                

def assert_arrangement(a: int | str ): 
    """ Assert whether the given arrangement is correct. 
    
    :param a: int, float, str - Type of given electrical arrangement. 
    
    :returns:
        - The correct arrangement name 
        - ``0`` which means ``False`` or a wrong given arrangements.   
    """
    
    for k, v in array_configuration.items(): 
        if a == k  or str(a).lower().strip() in ','.join (
                v[0]).lower() or a ==v[1]: 
            return  v[0][0].lower()
        
    return 0

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   