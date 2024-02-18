"""
Device control for the Thorlabs Filter Wheel.

This package contains the modules and classes to work with the 8SMC4 Filter Wheel from Thorlabs.

The main entry point for the user of this package is through the `FW8SMC4Proxy` class:

```python
>>> from egse.filterwheel.eksma.fw8smc4 import FilterWheel8SMC4Proxy
```

This class will connect to the control server of the filter wheel and provides all commands to
control this device and monitor its settings and status.

We have also provided a graphical user interface (GUI) to monitor and manipulate the filter wheel.
For this, execute the following command from the terminal. We assume hereby that your environment
and `PYTHONPATH` are set up properly.

```bash
$ python -m egse.filterwheel.eksma.fw8smc4_cs
```


"""

# Because of continued problems in generating the API documentation, we have decided to skip the
# filterwheel docs because of the `ximc` library:
#
# ```
# dlopen(/Users/rik/Documents/PyCharmProjects/plato-common-egse/src/egse/lib/ximc/libximc.framework/libximc, 0x0006):
# tried: '/Users/rik/Documents/PyCharmProjects/plato-common-egse/src/egse/lib/ximc/libximc.framework/libximc' (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64')),
# '/System/Volumes/Preboot/Cryptexes/OS/Users/rik/Documents/PyCharmProjects/plato-common-egse/src/egse/lib/ximc/libximc.framework/libximc' (no such file),
# '/Users/rik/Documents/PyCharmProjects/plato-common-egse-2653/src/egse/lib/ximc/libximc.framework/libximc' (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64')),
# '/Library/Frameworks/libximc.framework/libximc' (no such file),
# '/System/Library/Frameworks/libximc.framework/libximc' (no such file, not in dyld cache)
# Can\'t load libximc library. Please add all shared libraries to the appropriate places.
# It is decribed in detail in developers' documentation. On Linux make sure you installed libximc-dev package.
# make sure that the architecture of the system and the interpreter is the same
# ```
# See issue #2859
#

__pdoc__ = {
    # 'fw8smc4': False,
    'fw8smc4_devif': False,
    # 'fw8smc5': False,
    'fw8smc5_interface': False,
    'testpythonfw': False,
}
