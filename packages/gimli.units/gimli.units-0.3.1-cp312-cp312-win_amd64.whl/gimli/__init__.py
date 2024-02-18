"""""" # start delvewheel patch
def _delvewheel_patch_1_5_2():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'gimli.units.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_5_2()
del _delvewheel_patch_1_5_2
# end delvewheel patch

from gimli._udunits2 import Unit
from gimli._udunits2 import UnitEncoding
from gimli._udunits2 import UnitFormatting
from gimli._udunits2 import UnitNameError
from gimli._udunits2 import UnitStatus
from gimli._udunits2 import UnitSystem
from gimli._version import __version__
from gimli.errors import IncompatibleUnitsError

units = UnitSystem()

__all__ = [
    "__version__",
    "units",
    "IncompatibleUnitsError",
    "Unit",
    "UnitEncoding",
    "UnitFormatting",
    "UnitNameError",
    "UnitStatus",
    "UnitSystem",
]
