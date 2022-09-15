# -*- coding: utf-8 -*-
#   author: KLaurent <etanoyau@gmail.com>
#   Licence:  GPL-3.0 

from __future__ import print_function 

import functools
import inspect
import os
import copy 
import shutil
import warnings

import datetime 
import numpy as np
# import pandas as pd 
import  matplotlib.pyplot as plt 

from .typing import (
    Iterable,
    Optional,
    Callable ,
    T, F
)
from ._kalfeatlog import kalfeatlog

_logger = kalfeatlog.get_kalfeat_logger(__name__)

__docformat__='restructuredtext'

class refAppender (object): 
    """ Append the module docstring with reStructured Text references. 
    
    Indeed, when a `func` is decorated, it will add the reStructured Text 
    references as an appender to its reference docstring. So, sphinx 
    can auto-retrieve some replacing values found inline  from the 
    :doc:`kalfeat.documentation`. 
    
    .. |VES| replace:: Vertical Electrical Sounding 
    .. |ERP| replace:: Electrical Resistivity Profiling 
    
    Parameters
    ----------
    docref: str 
        Reference of the documentation for appending.
    
    Examples
    ---------
    >>> from kalfeat.documentation import __doc__ 
    >>> from kalfeat.tools import decorators
    >>> def donothing (): 
            ''' Im here to just replace the `|VES|` and `|RES|` values by their
            real meanings.'''
            pass 
    >>> decorated_donothing = decorators.refAppender(__doc__)(donothing) 
    >>> decorated_donothing.__doc__ 
    ... #new doctring appended and `|VES|` and `|ERP|` are replaced by 
    ... #Vertical Electrical Sounding and Electrical resistivity profiling 
    ... #during compilation in ReadTheDocs.
 
    """
    
    def __init__(self, docref= None ): 
        self.docref = docref 

    def __call__(self, cls_or_func): 
        return self.nfunc (cls_or_func)
    def nfunc (self, f):
        f.__doc__ += "\n" + self.docref or '' 
        setattr(f , '__doc__', f.__doc__)
        return  f 
  
    

class deprecated(object):
    """
    Used to mark functions, methods and classes deprecated, and prints 
    warning message when it called
    decorators based on https://stackoverflow.com/a/40301488 .

    Author: YingzhiGou
    Date: 20/06/2017
    """
    def __init__(self, reason):  # pragma: no cover
        if inspect.isclass(reason) or inspect.isfunction(reason):
            raise TypeError("Reason for deprecation must be supplied")
        self.reason = reason

    def __call__(self, cls_or_func):  # pragma: no cover
        if inspect.isfunction(cls_or_func):
            if hasattr(cls_or_func, 'func_code'):
                _code = cls_or_func.__code__
            else:
                _code = cls_or_func.__code__
            fmt = "Call to deprecated function or method {name} ({reason})."
            filename = _code.co_filename
            lineno = _code.co_firstlineno + 1

        elif inspect.isclass(cls_or_func):
            fmt = "Call to deprecated class {name} ({reason})."
            filename = cls_or_func.__module__
            lineno = 1

        else:
            raise TypeError(type(cls_or_func))

        msg = fmt.format(name=cls_or_func.__name__, reason=self.reason)

        @functools.wraps(cls_or_func)
        def new_func(*args, **kwargs):  # pragma: no cover
            import warnings
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            warnings.warn_explicit(msg, category=DeprecationWarning, 
                                   filename=filename, lineno=lineno)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return cls_or_func(*args, **kwargs)

        return new_func


class gdal_data_check(object):
  
    _has_checked = False
    _gdal_data_found = False
    _gdal_data_variable_resources = 'https://trac.osgeo.org/gdal/wiki/FAQInstallationAndBuilding#HowtosetGDAL_DATAvariable '
    _gdal_wheel_resources ='https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal'
    _gdal_installation_guide = 'https://opensourceoptions.com/blog/how-to-install-gdal-for-python-with-pip-on-windows/'


    def __init__(self, func, raise_error=False):
        """
        The decorator should only be used for the function that requires 
        gdal and gdal-data correctly.

        GDAL standas for Geospatial Data Abstraction Library. 
        It is a translator library for raster geospatial data formats.
        Its distribution includes a complete GDAL installation
        It will check whether the GDAL_DATA is set and the path
         in GDAL_DATA exists. If GDAL_DATA is not set, then try to
         use external program "gdal-config --datadir" to
        findout where the data files are installed.

        If failed to find the data file, then ImportError will be raised.

        :param func: function to be decorated
        
        """
  
        self._func = func
        if not self._has_checked:
            self._gdal_data_found = self._check_gdal_data()
            self._has_checked = True
        if not self._gdal_data_found:
            if(raise_error):
                raise ImportError(
                    "GDAL  is NOT installed correctly. "
                    f"GDAL wheel can be downloaded from {self._gdal_wheel_resources}"
                    " and use `pip install <path-to-wheel-file.whl>`"
                    "for installing. Get more details here: "
                    f" {self._gdal_installation_guide}."
                                  )
            else:
                warnings.warn(
                    "Ignore GDAL as it is not working. Will use `pyproj` "
                    f"OR download the GDAL wheel from {self._gdal_wheel_resources}"
                    " and use `pip install <path-to-wheel-file.whl>` "
                    "for GDAL installation. Get furher details via "
                    f"{self._gdal_installation_guide}"
                              )

    def __call__(self, *args, **kwargs):  # pragma: no cover
        return self._func(*args, **kwargs)

    def _check_gdal_data(self):
        if 'GDAL_DATA' not in os.environ:
            # gdal data not defined, try to define
            from subprocess import Popen, PIPE
            _logger.warning("GDAL_DATA environment variable is not set "
                            f" Please see {self._gdal_data_variable_resources}")
            try:
                # try to find out gdal_data path using gdal-config
                _logger.info("Trying to find gdal-data path ...")
                process = Popen(['gdal-config', '--datadir'], stdout=PIPE)
                (output, err) = process.communicate()
                exit_code = process.wait()
                output = output.strip()
                if exit_code == 0 and os.path.exists(output):
                    os.environ['GDAL_DATA'] = output
                    _logger.info("Found gdal-data path: {}".format(output))
                    return True
                else:
                    _logger.error(
                        "\tCannot find gdal-data path. Please find the"
                        " gdal-data path of your installation and set it to"
                        "\"GDAL_DATA\" environment variable. Please see "
                        f"{self._gdal_data_variable_resources} for "
                        "more information.")
                    return False
            except Exception:
                return False
        else:
            if os.path.exists(os.environ['GDAL_DATA']):
                _logger.info("GDAL_DATA is set to: {}".
                                  format(os.environ['GDAL_DATA']))

                try:
                    from osgeo import osr
                    from osgeo.ogr import OGRERR_NONE
                except:
                    _logger.error("Failed to load module osgeo; "
                                     "looks like GDAL is NOT working")
                    # print ("Failed to load module osgeo !!! ")

                    return False
                # end try

                return True
            else:
                _logger.error("GDAL_DATA is set to: {},"
                                   " but the path does not exist.".
                                   format(os.environ['GDAL_DATA']))
                return False

class redirect_cls_or_func(object) :
    """Used to redirected functions or classes. Deprecated functions  or class 
    can call others use functions or classes.
    
    Use new function or class to replace old function method or class with 
    multiple parameters.

    Author: @Daniel03
    Date: 18/10/2020
    
    """
    def __init__(self, *args, **kwargs) :
        """
        self.new_func_or_cls is just a message of deprecating 
        warning . It could be a name of new function  to let user 
        tracking its code everytime he needs . 

        """
        
        self._reason=[func_or_reason for func_or_reason in args
                      if type(func_or_reason)==str][0]
        if self._reason is None :
            
            raise TypeError(" Redirected reason must be supplied")
        

        self._new_func_or_cls = [func_or_reason for func_or_reason in 
                                 args if type(func_or_reason)!=str][0]

        if self._new_func_or_cls is None:
            raise Exception(
                " At least one argument must be a func_method_or class."
                            "\but it's %s."%type(self._new_func_or_cls))
            _logger.warn("\t first input argument argument must"
                              " be a func_method_or class."
                            "\but it's %s."%type(self._new_func_or_cls))
            

    def __call__(self, cls_or_func)  : #pragma :no cover

        if inspect.isfunction(self._new_func_or_cls) : 
            if hasattr(self._new_func_or_cls, 'func_code'):
                _code =self._new_func_or_cls.__code__
                lineno=_code.co_firstlineno+1
            else :
                # do it once the method is decorated method like staticmethods
                try:
                    _code =self._new_func_or_cls.__code__ 
                except : 
                    pass

            lineno=self._new_func_or_cls.__code__.co_firstlineno
            
            fmt="redirected decorated func/methods .<{reason}> "\
                "see line {lineno}."
            
        elif inspect.isclass(self._new_func_or_cls): 
            _code=self._new_func_or_cls.__module__
            # filename=os.path.basename(_code.co_filename)
            lineno= 1
            
            fmt="redirected decorated class :<{reason}> "\
                "see line {lineno}."
        else :
            # lineno=cls_or_func.__code__.co_firstlineno
            lineno= inspect.getframeinfo(inspect.currentframe())[1]
            fmt="redirected decorated method :<{reason}> "\
                "see line {lineno}."
        
        msg=fmt.format(reason = self._reason, lineno=lineno)
        # print(msg)
        _logger.info(msg)
            #count variables : func.__code__.co_argscounts
            #find variables in function : func.__code__.co_varnames
        @functools.wraps(cls_or_func)
        def new_func (*args, **kwargs):
            
            return cls_or_func(*args, **kwargs)
        return self._new_func_or_cls
        

class writef(object): 
    """
    Used to redirected functions or classes. Deprecated functions  or class can
    call others use functions or classes.
             
    Decorate function or class to replace old function method or class with 
    multiple parameters and export files into many other format. `.xlsx` ,
    `.csv` or regular format. Decorator mainly focus to export data to other
    files. Exported file can `regular` file or excel sheets. 
    
    :param reason: 
        Explain the "What to do?". Can be `write` or `convert`.
        
    :param from_: 
        Can be ``df`` or ``regular``. If ``df``, `func` is called and collect 
        its input argguments and write to appropriate extension. If `from_`is 
        ``regular``, Can be a simple data put on list of string ready 
        to output file into other format. 
    :type from_: str ``df`` or ``regular`` 
    
    :param to_: 
        Exported file extension. Can be excel sheeet (`.xlsx`, `csv`)
        or other kind of format. 
            
    :param savepath: 
        Give the path to save the new file written.
        
    *Author: @Daniel03*
    *Date: 09/07/2021*
        
    """
    
    def __init__(self, reason:Optional[str]=None,  from_:Optional[str]=None,
                 to:Optional[str]=None, savepath:Optional[str] =None, **kws): 
        self._logging =kalfeatlog().get_kalfeat_logger(self.__class__.__name__)
        
        self.reason = reason 
        self.from_=from_ 
        self.to= to
        
        self.refout =kws.pop('refout', None)
        self.writedfIndex =kws.pop('writeindex', False)
        
        self.savepath =savepath 
        
        
        for key in list(kws.keys()): 
            setattr(self, key, kws[key])

    def __call__(self, func):
        """ Call function and return new function decorated"""
        
        @functools.wraps(func)
        def decorated_func(*args, **kwargs): 
            """
            New decorated function and holds `func` args and kwargs arguments.
            :params args: positional arguments of `func`
            :param kwargs: keywords arguments of `func`. 
            
            """
            self._logging.info('Func <{}> decorated !'.format(func.__name__))
            
            cfw = 0     # write file type 
            
            for addf in ['savepath', 'filename']: 
                if not hasattr(self, addf): 
                    setattr(self, addf, None)
                    
            erp_time = '{0}_{1}'.format(datetime.datetime.now().date(), 
                            datetime.datetime.now().time())
            
            if self.refout is None : 
               self.refout = 'w-{0}'.format(
                   erp_time )
               
            if self.reason is None : 
                print('--> No reason is set. What do you want to do?'
                      ' `write` file or `convert` file into other format?.')
                return func(*args, **kwargs)
            
            if self.reason is not None : 
                if self.reason.lower().find('write')>=0 : 
                    cfw = 1 
                    if self.from_=='df': 
                        self.df , to_, refout_, savepath_, windex = func(*args,
                                                                 **kwargs)
                        fromdf =True
                        self.writedfIndex = windex
                         
            if fromdf is True and cfw ==1 : 
                if to_ is not None : 
                    self.to= '.'+ to_.replace('.','')
     
                else: 
                    self.to = '.csv'
                if refout_ is not None : 
                    self.refout =refout_
            
                self.refout = self.refout.replace(':','-') + self.to
                
                if savepath_ is not None: 
                    self.savepath =savepath_
                if self.to =='.csv': 
                    self.df.to_csv(self.refout, header=True,
                          index =self.writedfIndex)
                elif self.to =='.xlsx':
    
                    self.df.to_excel(self.refout , sheet_name='{0}'.format(
                        self.refout[: int(len(self.refout)/2)]),
                            index=self.writedfIndex) 
                             
                         
            # savepath 
            generatedfile = '_kalfeat{}_'.format(
                    datetime.datetime.now().time()).replace(':', '.')
            if self.savepath is None :
                self.savepath = savepath_(generatedfile)
            if self.savepath is not None :
                if not os.path.isdir(self.savepath): 
                    self.savepath = savepath_(generatedfile)
                try : 
                    shutil.move(os.path.join(os.getcwd(),self.refout) ,
                            os.path.join(self.savepath , self.refout))
                except : 
                    self.logging.debug("We don't find any path to save file.")
                else: 
                    print(
                    '--> reference output  file <{0}> is well exported to {1}'.
                          format(self.refout, self.savepath))
                    
            return func(*args, **kwargs)
        return decorated_func 
        

class docstring:
    """ Generate new doctring of a function or class by appending the doctring 
    of another function from the words considered as the startpoint `start` 
    to endpoint `end`.
    
    Sometimes two functions inherit the same parameters. Repeat the writing 
    of the same parameters is redundancy. So the most easier part is to 
    collect the doctring of the inherited function and paste to the new 
    function from the `startpoint`. 
    
    Parameters
    -----------
    func0: callable, 
        function to use its doctring 
    
    start: str 
        Value from which the new docstring should be start. 
    
    end: str 
        endpoint Value of the doctring. Stop considering point.
    

    Examples
    --------
    
    .. In the followings examples let try to append the `writedf` function
       from ``param reason`` (start) to `param to_` (end) to the 
       dostring to `predPlot` class. `predPlot` class class will holds new 
       doctring with writedf.__doc__ appended from `param reason` to 
       `param to_`.
        
    >>> from kalfeat.decorators import writedf , predPlot, docstring 
    >>> docs = doctring(writedf, start ='param reason', end='param to_')(predPlot)
    >>> docs.__doc__
    >>> predPlot.__doc__ # doc modified and holds the writedf docstring too.
    
    *Author: @Daniel03*
    *Date: 18/09/2021*
    """
    def __init__(self, func0, start='Parameters', end=None ):
        
        self.func0 = func0
        self.start =start 
        self.end =end 
        
    def __call__(self, func): 
        self._func =func 
        return self._decorator(self._func )
    
    def _decorator(self, func): 
        """ Collect the doctring of `func0` from `start` to `end` and 
        add to a new doctring of wrapper`.
        """
        func0_dstr = self.func0.__doc__ 
        # keet the only part you need
        if self.start is None: 
            start_ix =0
        else: 
            start_ix = func0_dstr.find(self.start) # index of start point
            
        if self.end is not None: 
            end_ix = func0_dstr.find(self.end)
            # remain_end_substring = func0_dstr[end_ix:]
            substring = func0_dstr[start_ix :end_ix]
        else : 
            substring = func0_dstr[start_ix :]
            end_ix = -1 
            
        if start_ix <0 : 
            warnings.warn(f'`{self.start}` not find in the given '
                          f'{self.func0.__name__!r} doctring` function will '
                          f'append all the doctring of {self.func0.__name__!r}'
                          ' by default.')
            start_ix =0 

        if end_ix <0 : 
            warnings.warn(f'`{self.end} not found in the given'
                      f' {self.func0.__name__!r} doctring` function will '
                      f'append all the doctring of {self.func0.__name__!r}'
                      ' thin the end by default.')
        
        if self.start is not None: 
            try:
                param_ix = func.__doc__.find(self.start)
            except AttributeError: 
                if inspect.isclass(func): 
                    fname = func.__class__.__name__
                else: fname = func.__name__
                # mean there is no doctrings.
                # but silent the warnings  
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    warnings.warn(" Object `%s` has none doctrings!`NoneType`"
                                  " object has no attribute `find`."%fname)
                return func
            # find end _ix and remove 
            if func.__doc__.find(self.end)>=0: 
                example_ix = func.__doc__.find(self.end)
   
                str_betw_param_example = func.__doc__[
                    param_ix:example_ix]
            else : 
                str_betw_param_example= func.__doc__[param_ix:]
                example_ix =None
             # remove --- `start`value and `\n` at the end of 
             # in func substring      
            str_betw_param_example = str_betw_param_example.replace(
                self.start +'\n', '').replace('-\n', '').replace('-', '')
            # now remove start point in 
            for i, item in enumerate(str_betw_param_example): 
                if item !=' ': 
                    str_betw_param_example= str_betw_param_example[i:]
                    break 
            # in the concat string to new docstring of func.
            func.__doc__ = func.__doc__[:param_ix] + f'{substring}'+\
                str_betw_param_example 
                
            if example_ix is not None: 
                func.__doc__+=  func.__doc__[example_ix:]
            # set new_attributes 
            setattr(func, '__doc__', func.__doc__)

        return func
            

class docAppender: 
    """
    Decorator to generate a new doctring from appending the other class docstrings. 
    
    Indeed from the startpoint <`from_`> and  the endpoint<`to`>, one can select 
    the part of the any function or class doctrings to append to the existing 
    doctring for a new doctring creation. This trip is useful to avoid 
    redundancing parameters definitions everywhere in the scripts.
    
    Parameters 
    -----------
    func0: callable, 
        Function or class to collect the doctring from. 
    from_: str 
        Reference word or expression to start the collection of the 
        necessary doctring from the `func0`. It is the startpoint. The 
        *default* is ``Parameters``. 
        
    to: str 
        Reference word to end the collection of the necessary part of the 
        docstring  of `func0`. It is the endpoint. The *default* is ``Returns``.
        
    insert: str, 
        Reference word or expression to insert the collected doctring from 
        the `func0` and append of the index of the `insert` word in `func`. 
        If not found in the `func` doctring, it should retun None so nothing 
        should be appended.  The *default* is ``Parameters``. 
    
    Examples
    ---------
    >>> from kalfeat.decorators import docAppender 
    >>> def func0 (*args, **kwargs): 
    ...        '''Im here so share my doctring. 
    ...        
    ...        Parameters 
    ...        -----------
    ...        * args: list, 
    ...            Collection of the positional arguments 
    ...        ** kwargs: dict 
    ...            Collection of keywords arguments 
    ...        Returns 
    ...        -------
    ...             None: nothing 
    ...        '''
    ...        pass 
    >>> def func(s, k=0): 
    ...        ''' Im here to append the docstring from func0
    ...        Parameters 
    ...        ----------
    ...        s: str , 
    ...            Any string value 
    ...        k: dict, 
    ...            first keyword arguments 
    ...            
    ...        Returns 
    ...        --------
    ...            None, I return nothing 
    ...        '''
    >>> deco = docAppender(func0 , from_='Parameters',
    ...                        to='Returns', insert ='---\\n')(func)
    >>> deco.__doc__
    ...
    
    Warnings 
    --------
    Be sure to append two doctrings with the same format. One may choose 
    either the sphinx or the numpy  doc formats. Not Mixing the both.  
    
    """
    insert_=('parameters',
            'returns',
            'raises', 
            'examples',
            'notes',
            'references', 
            'see also', 
            'warnings'
            )
    
    def __init__ (self,
                  func0: Callable[[F], F] ,
                  from_: str ='Parameters',
                 to: str ='Returns',
                 insertfrom: str = 'Parameters',
                 remove =True ): 
        self.func0 = func0 
        self.from_=from_ 
        self.to=to 
        self.remove= remove
        self.insert = insertfrom 
        
    def __call__(self, func): 
        self._func = copy.deepcopy(func )
        return self.make_newdoc (self._func)
    
    def  make_newdoc(self, func): 
        """ make a new docs from the given class of function """
 
        def sanitize_docstring ( strv): 
            """Sanitize string values and force the string to be 
            on the same level for parameters and the arguments of the 
            parameters. 
            :param strv: str 
            
            return a new string sanitized that match the correct spaces for 
            the sphinx documentation.
            
            """
            if isinstance(strv, str): 
                strv = strv.split('\n')
            # remove the ''  in the first string
            if strv[0].strip() =='':strv=strv[1:] 
            # get the first occurence for parameters definitions 
            ix_ = 0 ; 
            for ix , value in enumerate (strv): 
                if (value.lower().find(':param') >=0) or (value.lower(
                        ).find('parameters')>=0): 
                    ix_ = ix ; break 
            # Put all explanations in the same level 
            # before the parameters 
            for k in range(ix_ +1): 
                strv[k]= strv[k].strip() 
        
            for ii, initem in enumerate (strv): 
                for v in self.insert_: 
                    if initem.lower().find(v)>=0: 
                        initem= initem.strip() 
                        strv[ii]= initem
                        break 
    
                if '--' in initem or (':' in initem and len(initem) < 50) : 
                    strv[ii]= initem.strip() 
                elif (initem.lower() not in self.insert_) and ii > ix_:  
                    strv[ii]='    ' + initem.strip() 
            
            return '\n'.join(strv)  
 
        # get the doctring from the main func0 
        func0_dstr = self.func0.__doc__ 
        # select the first occurence and remove '----' if exists 
        if self.from_ is None: 
            warnings.warn('Argument `from_` is missing. Should be the first'
                          f' word of {self.func0.__name__!r} doctring.')
            self.from_ = func0_dstr.split()[0]
            
        from_ix = func0_dstr.find(self.from_)
        func0_dstr = func0_dstr [from_ix:]
        # remove the first occurence of the from_ value and --- under if exists. 
        # in the case where from =':param' remove can be set to False 
        if self.remove: 
            func0_dstr = func0_dstr.replace(self.from_, '', 1).replace('-', '')
        # get the index of 'to' or set None if not given   
        # now we are selected the part and append to the 
        # existing doc func where do you want to insert 
        to_ix = func0_dstr.find (self.to ) if self.to is not None else None 
        func0_dstr= func0_dstr [:to_ix if to_ix >=0 else None]
       
        if self.insert.lower() not in (self.insert_): 
            warnings.warn(f"It's seems the given  {self.insert!r} for docstring"
                          f" insertion is missing to {self.insert_} list")
        
        in_ix =  self._func.__doc__.lower().find(self.insert.lower())
        # assert  whether the given value insert from exists . 
        if in_ix < 0 : 
            warnings.warn(f"Insert {self.insert!r} value is not found in the "
                          "{'class' if inspect.isclass(self._func) else 'function'")
        # split the string with `\n` 
        # and loop to find the first occurence 
        # by default skip the next item which could be '----' 
        # and insert to the list next point 
        func0_dstr = func0_dstr.split('\n')
        finalstr = self._func.__doc__.split('\n') 
        
        rpop(func0_dstr) 
        func0_dstr =  '\n'.join(func0_dstr)    
        for ii, oc in enumerate(finalstr) : 
            if oc.lower().find(self.insert.lower()) >=0 : 
                finalstr.insert (ii+2, func0_dstr)
                finalstr = '\n'.join(finalstr);break 
        
        setattr(func, '__doc__', sanitize_docstring (finalstr))
        
        return func 
    
class docSanitizer: 
    """Decorator to clean the doctring and  set all values of sections to 
    the same level. 
    
    It sanitizes the doctring for the use of sphinx documentation. 
    
    Examples
    --------
    >>> from kalfeat.decorators import docSanitizer 
    >>> def messdocfunc(): 
    ...        '''My doctring is mess. I need to be polished and well arranged.
    ...        
    ...        Im here to sanitize the mess doctring. 
    ...        
    ...        Parameters
    ...        ----------
    ...                * args: list, 
    ...                    Collection of the positional arguments 
    ...                ** kwargs: dict 
    ...                    Collection of keywords arguments 
    ...
    ...        * kwargs: list,
    ...        Collection of the keyword arguments
    ...        
    ...        Warnings
    ...        --------
    ...        Let check for warnings string ... 
    ...        
    ...       '''
    ...       pass
    >>> cleandocfunc = docSanitizer()(messfocfunc)
    >>> print(cleandocfunc.__doc__)
    ... '''
    ...    My doctring is mess. I need to be polished and well arranged.
    ...
    ...    Parameters
    ...    ----------
    ...    * args: list,
    ...       Collection of the positional arguments
    ...    ** kwargs: dict
    ...        Collection of keywords arguments
    ...    * kwargs: list,
    ...        Collection of the keyword arguments
    ...    '''
    
    """
    
    insert_= ('parameters','returns','raises', 'examples','notes',
            'references', 'see also', 'warnings', ':param', ':rtype', 
            )
    
    def __call__(self, func): 
        
        func =copy.deepcopy(func)
        docstring = copy.deepcopy(func.__doc__) 
        
        if isinstance(docstring , str): 
            docstring = docstring .split('\n')
        # remove the ''  in the first string
        if docstring [0].strip() =='':docstring =docstring [1:] 
        # get the first occurence for parameters definitions 
        # and separate the doctring into two parts: descriptions 
        #and corpus doctring as the remainings 
        
        ix_ = 0  
        for ix , value in enumerate (docstring ): 
            if (value.lower().find(':param') >=0) or (value.lower(
                    ).find('parameters')>=0): 
                ix_ = ix ; break 
            
        #-->  sanitize the descriptions part 
        description =docstring [: ix_] ; 
        # before the parameters 
        for k in range(len(description)): 
            description [k]= description [k].strip() 
         # remove at the end of description the blanck space '\n' 
        description = description[:-1] if  description[-1].strip(
            )== ''  else description
      
        # --> work with the corpus docstrings 
        # get indexes for other sections and removes spaces 
        docstring = docstring [ix_:]
        rpop (docstring)
        ixb = len(docstring)
        for ind , values in enumerate (docstring): 
            if values.lower().strip() in (
                    'examples', 'see also', 'warnings', 
                     'notes', 'references'): 
                ixb = ind ; break 
        # all values in same level 
        for k in range(ixb, len(docstring)): 
            docstring [k]= docstring [k].strip() 
        for ii, initem in enumerate (docstring ): 
            for v in self.insert_: 
                if initem.lower().find(v)>=0: 
                    initem= initem.strip() 
                    docstring [ii]= initem
                    break 
            if '--' in initem or (
                    ':' in initem and len(initem) < 50
                    ) or ix_>=ixb : 
                docstring [ii]= initem.strip() 
            elif (initem.lower() not in self.insert_
                  ) and ix_< ii < ixb:  
                docstring [ii]='    ' + initem.strip() 
        # add  blanck line from indexes list ixs 
        ixs=list()
        for k, item in enumerate (docstring): 
            for param in self.insert_[:-2]: 
                if item.lower().strip() == param:  
                    ixs.append(k)
                    break   
        ki =0  
        for k in ixs : 
            docstring.insert (k+ki, '')  
            ki+=1 # add number of insertions 
            
        # --> combine the descriptions and docstring and set attributes 
        setattr(func, '__doc__' , '\n'.join(description + docstring ))  
          
        return  func
        
###############################################################################
# decorators utilities 
def rpop(listitem): 
    """ remove all blank line in the item list. 
    :param listitem: list- list of the items and pop all 
    the existing blanck lines. """
    # now pop all the index for blanck line 
    isblanck = False 
    for ii, item  in enumerate (listitem) : 
        if item.strip()=='': 
            listitem.pop(ii)
            isblanck =True 
    return rpop(listitem) if isblanck else False  










































            

        
            
    