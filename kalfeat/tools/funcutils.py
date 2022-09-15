# -*- coding: utf-8 -*-
#   author: KLaurent <etanoyau@gmail.com>
#   Licence:  GPL-3.0 

from __future__ import annotations 

import os 
import sys 
import inspect 
import subprocess 
import warnings

import numpy as np 
import pandas as pd 

from .._kalfeatlog import kalfeatlog
from ..typing import ( 
    Tuple,
    Dict,
    Any,
    Array,
    F,
    T,
    List ,
    DataFrame, 
    Sub,
    )

_logger = kalfeatlog.get_kalfeat_logger(__name__)

def smart_strobj_recognition(
        name: str  ,
        container: List | Tuple | Dict[Any, Any ],
        stripitems: str | List | Tuple = '_', 
        deep: bool = False,  
) -> str : 
    """ Find the likelihood word in the whole containers and 
    returns the value.
    
    :param name: str - Value of to search. I can not match the exact word in 
    the `container`
    :param container: list, tuple, dict- container of the many string words. 
    :param stripitems: str - 'str' items values to sanitize the  content 
        element of the dummy containers. if different items are provided, they 
        can be separated by ``:``, ``,`` and ``;``. The items separators 
        aforementioned can not  be used as a component in the `name`. For 
        isntance:: 
            
            name= 'dipole_'; stripitems='_' -> means remove the '_'
            under the ``dipole_``
            name= '+dipole__'; stripitems ='+;__'-> means remove the '+' and
            '__' under the value `name`. 
        
    :param deep: bool - Kind of research. Go deeper by looping each items 
         for find the initials that can fit the name. Note that, if given, 
         the first occurence should be consider as the best name... 
         
    :return: Likelihood object from `container`  or Nonetype if none object is
        detected.
        
    :Example:
        >>> from kalfeat.tools.funcutils import smart_strobj_recognition
        >>> from kalfeat.methods import ResistivityProfiling 
        >>> rObj = ResistivityProfiling(AB= 200, MN= 20,)
        >>> smart_strobj_recognition ('dip', robj.__dict__))
        ... None 
        >>> smart_strobj_recognition ('dipole_', robj.__dict__))
        ... dipole 
        >>> smart_strobj_recognition ('dip', robj.__dict__,deep=True )
        ... dipole 
        >>> smart_strobj_recognition (
            '+_dipole___', robj.__dict__,deep=True , stripitems ='+;_')
        ... 'dipole'
        
    """

    stripitems =_assert_all_types(stripitems , str, list, tuple) 
    container = _assert_all_types(container, list, tuple, dict)
    ix , rv = None , None 
    
    if isinstance (stripitems , str): 
        for sep in (':', ",", ";"): # when strip ='a,b,c' seperated object
            if sep in stripitems:
                stripitems = stripitems.strip().split(sep) ; break
        if isinstance(stripitems, str): 
            stripitems =[stripitems]
            
    # sanitize the name. 
    for s in stripitems :
        name = name.strip(s)     
        
    if isinstance(container, dict) : 
        #get only the key values and lower them 
        container_ = list(map (lambda x :x.lower(), container.keys())) 
    else :
        # for consistency put on list if values are in tuple. 
        container_ = list(container)
        
    # sanitize our dummny container item ... 
    #container_ = [it.strip(s) for it in container_ for s in stripitems ]
    if name.lower() in container_: 
        ix = container_.index (name)
        
    if deep and ix is None:
        # go deeper in the search... 
        for ii, n in enumerate (container_) : 
            if n.find(name.lower())>=0 : 
                ix =ii ; break 
    
    if ix is not None: 
        if isinstance(container, dict): 
            rv= list(container.keys())[ix] 
        else : rv= container[ix] 

    return  rv 

def repr_callable_obj(obj: F  ): 
    """ Represent callable objects. 
    
    Format class, function and instances objects. 
    
    :param obj: class, func or instances
        object to format. 
    :Raises: TypeError - If object is not a callable or instanciated. 
    
    :Examples: 
        >>> from kalfeat.tools.funcutils import repr_callable_obj
        >>> from kalfeat.methods.dc import (
            ElectricalMethods, ResistivityProfiling)
        >>> callable_format(ElectricalMethods)
        ... 'ElectricalMethods(AB= None, arrangement= schlumberger,
                area= None, MN= None, projection= UTM, datum= WGS84,
                epsg= None, utm_zone= None, fromlog10= False)'
        >>> callable_format(ResistivityProfiling)
        ... 'ResistivityProfiling(station= None, dipole= 10.0, 
                auto_station= False, kws= None)'
        >>> robj= ResistivityProfiling (AB=200, MN=20, station ='S07')
        >>> repr_callable_obj(robj)
        ... 'ResistivityProfiling(AB= 200, MN= 20, arrangememt= schlumberger,
                utm_zone= None, projection= UTM, datum= WGS84, epsg= None, 
                area= None, fromlog10= False, dipole= 10.0, station= S07)'
        >>> repr_callable_obj(robj.fit)
        ... 'fit(data= None, kws= None)'
    """
    
    # inspect.formatargspec(*inspect.getfullargspec(cls_or_func))
    if not hasattr (obj, '__call__') and not hasattr(obj, '__dict__'): 
        raise TypeError (
            f'Format only callabe objects: {type (obj).__name__!r}')
        
    if hasattr (obj, '__call__'): 
        cls_or_func_signature = inspect.signature(obj)
        objname = obj.__name__
        PARAMS_VALUES = {k: None if v.default is (inspect.Parameter.empty 
                         or ...) else v.default 
                    for k, v in cls_or_func_signature.parameters.items()
                    # if v.default is not inspect.Parameter.empty
                    }
    elif hasattr(obj, '__dict__'): 
        objname=obj.__class__.__name__
        PARAMS_VALUES = {k:v  for k, v in obj.__dict__.items() 
                         if not (k.endswith('_') or k.startswith('_'))}

    return   str (objname) + '(' + str (PARAMS_VALUES).replace (
            '{', '').replace('}', '').replace(
                ':', '=').replace("'", '') + ')'

def accept_types (*objtypes: list , 
                  format: bool = False
                  ) -> List[str] | str : 
    """ List the type format that can be accepted by a function. 
    
    :param objtypes: List of object types.
    
    :param format: bool - format the list of the name of objects.
    
    :return: list of object type names or str of object names. 
    
    :Example: 
        >>> import numpy as np; import pandas as pd 
        >>> from kalfeat.tools.funcutils import accept_types
        >>> accept_types (pd.Series, pd.DataFrame, tuple, list, str)
        ... "'Series','DataFrame','tuple','list' and 'str'"
        >>> atypes= accept_types (
            pd.Series, pd.DataFrame,np.ndarray, format=True )
        ..."'Series','DataFrame' and 'ndarray'"
    """
    return smart_format(
        [f'{o.__name__}' for o in objtypes]
        ) if format else [f'{o.__name__}' for o in objtypes] 

def read_from_excelsheets(erp_file: str = None ) -> List[DataFrame]: 
    
    """ Read all Excelsheets and build a list of dataframe of all sheets.
   
    :param erp_file:
        Excell workbooks containing `erp` profile data.
        
    :return: A list composed of the name of `erp_file` at index =0 and the 
      datataframes.
      
    """
    
    allfls:Dict [str, Dict [T, List[T]] ] = pd.read_excel(
        erp_file, sheet_name=None)
    
    list_of_df =[os.path.basename(os.path.splitext(erp_file)[0])]
    for sheets , values in allfls.items(): 
        list_of_df.append(pd.DataFrame(values))

    return list_of_df 

def check_dimensionality(obj, data, z, x):
    """ Check dimensionality of data and fix it.
    
    :param obj: Object, can be a class logged or else.
    
    :param data: 2D grid data of ndarray (z, x) dimensions.
    
    :param z: array-like should be reduced along the row axis.
    
    :param x: arraylike should be reduced along the columns axis.
    
    """
    def reduce_shape(Xshape, x, axis_name=None): 
        """ Reduce shape to keep the same shape"""
        mess ="`{0}` shape({1}) {2} than the data shape `{0}` = ({3})."
        ox = len(x) 
        dsh = Xshape 
        if len(x) > Xshape : 
            x = x[: int (Xshape)]
            obj._logging.debug(''.join([
                f"Resize {axis_name!r}={ox!r} to {Xshape!r}.", 
                mess.format(axis_name, len(x),'more',Xshape)])) 
                                    
        elif len(x) < Xshape: 
            Xshape = len(x)
            obj._logging.debug(''.join([
                f"Resize {axis_name!r}={dsh!r} to {Xshape!r}.",
                mess.format(axis_name, len(x),'less', Xshape)]))
        return int(Xshape), x 
    
    sz0, z = reduce_shape(data.shape[0], 
                          x=z, axis_name ='Z')
    sx0, x =reduce_shape (data.shape[1],
                          x=x, axis_name ='X')
    data = data [:sz0, :sx0]
    
    return data , z, x 

def is_installing (module, upgrade=True , DEVNULL=False,
                  action=True, verbose =0, **subpkws): 
    """ Install or uninstall a module using the subprocess under the hood.
    
    :param module: str, module name.
    
    :param upgrade:bool, install the lastest version.
    
    :param verbose:output a message.
    
    :param DEVNULL: decline the stdoutput the message in the console.
    
    :param action: str, install or uninstall a module.
    
    :param subpkws: additional subprocess keywords arguments.
    
    :Example: 
        >>> from pycsamt.tools.funcutils import is_installing
        >>> is_installing(
            'tqdm', action ='install', DEVNULL=True, verbose =1)
        >>> is_installing(
            'tqdm', action ='uninstall', verbose =1)
    """
    #implement pip as subprocess 
    # refer to https://pythongeeks.org/subprocess-in-python/
    if not action: 
        if verbose > 0 :
            print("---> No action `install`or `uninstall`"
                  f" of the module {module!r} performed.")
        return action  # DO NOTHING 
    
    MOD_IMP=False 

    action_msg ='uninstallation' if action =='uninstall' else 'installation' 

    if action in ('install', 'uninstall', True) and verbose > 0:
        print(f'---> Module {module!r} {action_msg} will take a while,'
              ' please be patient...')
        
    cmdg =f'<pip install {module}> | <python -m pip install {module}>'\
        if action in (True, 'install') else ''.join([
            f'<pip uninstall {module} -y> or <pip3 uninstall {module} -y ',
            f'or <python -m pip uninstall {module} -y>.'])
        
    upgrade ='--upgrade' if upgrade else '' 
    
    if action == 'uninstall':
        upgrade= '-y' # Don't ask for confirmation of uninstall deletions.
    elif action in ('install', True):
        action = 'install'

    cmd = ['-m', 'pip', f'{action}', f'{module}', f'{upgrade}']

    try: 
        STDOUT = subprocess.DEVNULL if DEVNULL else None 
        STDERR= subprocess.STDOUT if DEVNULL else None 
    
        subprocess.check_call(
            [sys.executable] + cmd, stdout= STDOUT, stderr=STDERR,
                              **subpkws)
        if action in (True, 'install'):
            # freeze the dependancies
            reqs = subprocess.check_output(
                [sys.executable,'-m', 'pip','freeze'])
            [r.decode().split('==')[0] for r in reqs.split()]
            _logger.info( f"{action_msg.capitalize()} of `{module}` "
                         "and dependancies was successfully done!") 
        MOD_IMP=True
        
    except: 
        _logger.error(f"Failed to {action} the module =`{module}`.")
        
        if verbose > 0 : 
            print(f'---> Module {module!r} {action_msg} failed. Please use'
                f' the following command: {cmdg} to manually do it.')
    else : 
        if verbose > 0: 
            print(f"{action_msg.capitalize()} of `{module}` "
                      "and dependancies was successfully done!") 
        
    return MOD_IMP 


def smart_format(iter_obj): 
    """ Smart format iterable ob.
    
    :param iter_obj: iterable obj 
    
    :Example: 
        >>> from kalfeat.tools.funcutils import smart_format
        >>> smart_format(['model', 'iter', 'mesh', 'data'])
        ... 'model','iter','mesh' and 'data'
    """
    str_litteral =''
    try: 
        iter(iter_obj) 
    except:  return f"{iter_obj}"
    
    iter_obj = [str(obj) for obj in iter_obj]
    if len(iter_obj) ==1: 
        str_litteral= ','.join([f"{i!r}" for i in iter_obj ])
    elif len(iter_obj)>1: 
        str_litteral = ','.join([f"{i!r}" for i in iter_obj[:-1]])
        str_litteral += f" and {iter_obj[-1]!r}"
    return str_litteral

def make_introspection(Obj: object , subObj: Sub[object])->None: 
    """ Make introspection by using the attributes of instance created to 
    populate the new classes created.
    
    :param Obj: callable 
        New object to fully inherits of `subObject` attributes.
        
    :param subObj: Callable 
        Instance created.
    """
    # make introspection and set the all  attributes to self object.
    # if Obj attribute has the same name with subObj attribute, then 
    # Obj attributes get the priority.
    for key, value in  subObj.__dict__.items(): 
        if not hasattr(Obj, key) and key  != ''.join(['__', str(key), '__']):
            setattr(Obj, key, value)
            
def cpath (savepath=None , dpath=None): 
    """ Control the existing path and create one of it does not exist.
    
    :param savepath: Pathlike obj, str 
    :param dpath: str, default pathlike obj
    
    """
    if dpath is None:
        file, _= os.path.splitext(os.path.basename(__file__))
        dpath = ''.join(['_', file,
                         '_']) #.replace('.py', '')
    if savepath is None : 
        savepath  = os.path.join(os.getcwd(), dpath)
        try:os.mkdir(savepath)
        except: pass 
    if savepath is not None:
        try :
            if not os.path.isdir(savepath):
                os.mkdir(savepath)#  mode =0o666)
        except : pass 
    return savepath   
  


def sPath (name_of_path:str):
    """ Savepath func. Create a path  with `name_of_path` if path not exists.
    
    :param name_of_path: str, Path-like object. If path does not exist,
        `name_of_path` should be created.
    """
    
    try :
        savepath = os.path.join(os.getcwd(), name_of_path)
        if not os.path.isdir(savepath):
            os.mkdir(name_of_path)#  mode =0o666)
    except :
        warnings.warn("The path seems to be existed!")
        return
    return savepath 


def format_notes(text:str , cover_str: str ='~', inline=70, **kws): 
    """ Format note 
    :param text: Text to be formated.
    
    :param cover_str: type of ``str`` to surround the text.
    
    :param inline: Nomber of character before going in liine.
    
    :param margin_space: Must be <1 and expressed in %. The empty distance 
        between the first index to the inline text 
    :Example: 
        
        >>> from kalfeat.tools import funcutils as func 
        >>> text ='Automatic Option is set to ``True``.'\
            ' Composite estimator building is triggered.' 
        >>>  func.format_notes(text= text ,
        ...                       inline = 70, margin_space = 0.05)
    
    """
    
    headnotes =kws.pop('headernotes', 'notes')
    margin_ratio = kws.pop('margin_space', 0.2 )
    margin = int(margin_ratio * inline)
    init_=0 
    new_textList= []
    if len(text) <= (inline - margin): 
        new_textList = text 
    else : 
        for kk, char in enumerate (text): 
            if kk % (inline - margin)==0 and kk !=0: 
                new_textList.append(text[init_:kk])
                init_ =kk 
            if kk ==  len(text)-1: 
                new_textList.append(text[init_:])
  
    print('!', headnotes.upper(), ':')
    print('{}'.format(cover_str * inline)) 
    for k in new_textList:
        fmtin_str ='{'+ '0:>{}'.format(margin) +'}'
        print('{0}{1:>2}{2:<51}'.format(fmtin_str.format(cover_str), '', k))
        
    print('{0}{1:>51}'.format(' '* (margin -1), cover_str * (inline -margin+1 ))) 
    


def round_dipole_length(value, round_value =5.): 
    """ 
    small function to graduate dipole length 5 to 5. Goes to be reality and 
    simple computation .
    
    :param value: value of dipole length 
    :type value: float 
    
    :returns: value of dipole length rounded 5 to 5 
    :rtype: float
    """ 
    mm = value % round_value 
    if mm < 3 :return np.around(value - mm)
    elif mm >= 3 and mm < 7 :return np.around(value -mm +round_value) 
    else:return np.around(value - mm +10.)
    

def _isin (
        arr: Array | List [float] ,
        subarr: Sub [Array] |Sub[List[float]] | float 
) -> bool : 
    """ Check whether the subset array `subcz` is in  `cz` array. 
    
    :param arr: Array-like - Array of item elements 
    :param subarr: Array-like, float - Subset array containing a subset items.
    :return: True if items in  test array `subarr` are in array `arr`. 
    
    """
    arr = np.array (arr );  subarr = np.array(subarr )

    return True if True in np.isin (arr, subarr) else False 

def _assert_all_types (
        obj: object , 
        *expected_objtype: type 
 ) -> object: 
    """ Quick assertion of object type. Raise an `TypeError` if 
    wrong type is given."""
    # if np.issubdtype(a1.dtype, np.integer): 
    if not isinstance( obj, expected_objtype): 
        raise TypeError (
            f'Expected {smart_format(tuple (o.__name__ for o in expected_objtype))}'
            f' type{"s" if len(expected_objtype)>1 else ""} '
            f'but `{type(obj).__name__}` is given.')
            
    return obj 

  
def savepath_ (nameOfPath): 
    """
    Shortcut to create a folder 
    :param nameOfPath: Path name to save file
    :type nameOfPath: str 
    
    :return: 
        New folder created. If the `nameOfPath` exists, will return ``None``
    :rtype:str 
        
    """
 
    try :
        savepath = os.path.join(os.getcwd(), nameOfPath)
        if not os.path.isdir(savepath):
            os.mkdir(nameOfPath)#  mode =0o666)
    except :
        warnings.warn("The path seems to be existed !")
        return
    return savepath 
     









    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
        