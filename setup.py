"""
scikit-misc

Miscellaneous tools for data analysis and scientific computing.
"""
import os
import sys
import builtins
import subprocess


# BEFORE importing setuptools, remove MANIFEST. Otherwise it may
# not be properly updated when the contents of directories change
# (true for distutils, not sure about setuptools).
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

# This is a bit hackish: we are setting a global variable so that
# the main skmisc __init__ can detect if it is being loaded by the
# setup routine, to avoid attempting to load components that aren't
# built yet. Copied from numpy
builtins.__SKMISC_SETUP__ = True


def generate_cython():
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable,
                         os.path.join(cwd, 'tools', 'cythonize.py'),
                         'skmisc'],
                        cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('skmisc')
    return config


def prepare_for_setup():
    cwd = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(cwd, 'PKG-INFO')):
        # Generate Cython sources, unless building from source release
        generate_cython()


def setup_package():
    # versioneer needs numpy cmdclass
    from numpy.distutils.core import setup, numpy_cmdclass
    metadata = dict(
        name='scikit-misc',
        cmdclass=numpy_cmdclass,
        configuration=configuration
    )
    setup(**metadata)


if __name__ == '__main__':
    prepare_for_setup()
    setup_package()

    del builtins.__SKMISC_SETUP__
