#!/usr/bin/env python

import kalfeat
import os 

# Check for setuptools package:

try:
    from setuptools import setup
except ImportError:
    setuptools = False
    from distutils.core import setup
else:
    setuptools = True


with open(os.path.join(os.path.abspath('.'), 
                       'README.md'), 'r') as fm:

    LONG_DESCRIPTION =fm.read()

setup_kwargs = {}
setup_kwargs['entry_points'] = {
                    'console_scripts':[
                             'occam2d_build_in = kalfeat.gui.oc2d_bdin:main',
                             'write_avg2edi= kalfeat.gui.wa2edi:main',

                     ]
     }
                     
                        
# But many people will not have setuptools installed, so we need to handle
# the default Python installation, which only has Distutils:

if setuptools is False:
    # Different script specification style for ordinary Distutils:
    setup_kwargs['scripts'] = [
        s.split(' = ')[1].replace('.', '/').split(':')[0] + '.py' for s in 
        setup_kwargs['entry_points']['console_scripts']]
    del setup_kwargs['entry_points']

    # "You must explicitly list all packages in packages: the Distutils will not
    # recursively scan your source tree looking for any directory with an
    # __init__.py file"

setup_kwargs['packages'] = [ 
                            'kalfeat',
                            'kalfeat.method',
                            'kalfeat.tools.core',
                            ]
# force install kalfeat. Once kalfeat is installed , pyyaml and pyproj 
# should already installed too. 
     
setup_kwargs['install_requires'] = ['numpy>=1.8.1',
                                     'scipy>=0.14.0',
                                     'matplotlib',
                                     'pyyaml',
                                     'pyproj',
                                     'configparser', 
                                     'tqdm']
                                     
setup_kwargs['python_requires'] ='>=3.7'

authors =["Kouadio Laurent"]
authors_emails =['etanoyau@gmail.com']
setup(
 	name="kalfeat",
 	version=kalfeat.__version__,
 	author=' '.join([aa for aa in authors]),
    author_email='etanoyau@gmail.com',
    maintainer="Kouadio K. Laurent",
    maintainer_email='etanoyau@gmail.com',
 	description="A light package for fast detecting the geo-electrical features",
 	long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/WEgeophysics/kalfeat",
    project_urls={
        "API Documentation"  : "https://kalfeat.readthedocs.io/en/master/",
        "Home page" : "https://github.com/WEgeophysics/kalfeat/wiki",
        "Bugs tracker": "https://github.com/WEgeophysics/kalfeat/issues",
        # "Installation guide" : "https://github.com/WEgeophysics/kalfeat/wiki/kalfeat-installation-guide-for-Windows--and-Linux", 
        # "User guide" : "https://github.com/WEgeophysics/kalfeat/blob/develop/docs/kalfeat%20User%20Guide.pdf",
        },
 	#data_files=[('', ['kalfeat/utils/epsg.npy',]),], #this will install datafiles in wearied palce such as ~/.local/
 	include_package_data=True,
 	license="GNU LESSER GENERAL PUBLIC LICENSE v3",
 	classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        # "Topic :: Software Development :: Build Tools",
        #"License :: OSI Approved :: GNU License",
        'Topic :: Scientific/Engineering :: Geophysics',
        'Topic :: Scientific/Engineering :: Geosciences',
        
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Operating System :: OS Independent",
        ],
    keywords="hydrogeophysic, groundwater, exploration, csamt",
    #package_dir={"": "kalfeat"},  # Optional
    package_data={'kalfeat': [
                            'utils/p.configlog.yml', 
                            'utils/espg.npy',
                            '_loggerfiles/*.txt',
                            
                            ], 
                    "":[
                        'data/ves/*', 
                        'data/erp/*', 
                        ]
                  },
    
 	**setup_kwargs
)
























