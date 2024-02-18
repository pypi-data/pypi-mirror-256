PROGRAM = "zero"
DESCRIPTION = "Linear circuit simulator"

# Get package version.
try:
    from ._version import version as __version__
except ImportError:
    raise RuntimeError("Could not find _version.py. Ensure you have run setup.")

from .config import ZeroConfig
CONF = ZeroConfig()

# Update Matplotlib options with overrides from config.
from matplotlib import rcParams
rcParams.update(CONF["plot"]["matplotlib"])

# Make some classes available from the top level package.
# This is placed here because dependent imports need the code above.
from .components import Circuit, Resistor, Capacitor, Inductor, OpAmp
