"""Electronic circuit class to which linear components can be added and
on which simulations can be performed."""

import logging
from copy import deepcopy
import numpy as np

from .config import ZeroConfig, OpAmpLibrary
from .components import (Resistor, Capacitor, Inductor, OpAmp, Node, ElementNotFoundError,
                         ComponentNotFoundError, NodeNotFoundError, NoiseNotFoundError)
from .tools import validate_name

LOGGER = logging.getLogger(__name__)
CONF = ZeroConfig()
LIBRARY = OpAmpLibrary()


class Circuit:
    """An electronic circuit."""

    def __init__(self, name=None):
        if name is not None:
            validate_name(name)

        self.name = name
        self.nodes = ["gnd"]
        self.components = {}  # name -> object

    def __getitem__(self, key):
        return self.components[key]

    def __contains__(self, key):
        return key in self.components

    @property
    def nnodes(self):
        return len(self.nodes)

    @property
    def nvsources(self):
        return len(self.voltage_sources)

    @property
    def voltage_sources(self):
        return [component for component in self.components.values() if component.GENERATES_VOLTAGE]

    def _create_node(self, name, exist_ok=False):
        """Create a new circuit node."""
        validate_name(name)
        final_name = name.casefold()

        if final_name in self.nodes:
            if not exist_ok:
                raise ValueError(f"Node {repr(name)} already exists.")
        else:
            self.nodes.append(final_name)

        return self.nodes.index(final_name)

    def add_resistor(self, name, value, n1, n2):
        """Add a resistor to the circuit."""
        nn1 = self._create_node(n1, exist_ok=True)
        nn2 = self._create_node(n2, exist_ok=True)
        resistor = Resistor(name, value, nn1, nn2)
        self.components[resistor.name] = resistor

    def add_capacitor(self, name, value, n1, n2):
        """Add a capacitor to the circuit."""
        nn1 = self._create_node(n1, exist_ok=True)
        nn2 = self._create_node(n2, exist_ok=True)
        capacitor = Capacitor(name, value, nn1, nn2)
        self.components[capacitor.name] = resistor

    def add_inductor(self, name, value, n1, n2):
        """Add an inductor to the circuit."""
        nn1 = self._create_node(n1, exist_ok=True)
        nn2 = self._create_node(n2, exist_ok=True)
        inductor = Inductor(name, value, nn1, nn2)
        self.components[inductor.name] = resistor

    def add_opamp(self, name, n1, n2, n3, **kwargs):
        """Add an op-amp to the circuit."""
        nn1 = self._create_node(n1, exist_ok=True)
        nn2 = self._create_node(n2, exist_ok=True)
        nn3 = self._create_node(n3, exist_ok=True)
        opamp = OpAmp(name, nn1, nn2, nn3, **kwargs)
        self.components[opamp.name] = opamp

    def add_library_opamp(self, name, model, n1, n2, n3, **kwargs):
        """Add a library op-amp to the circuit."""
        # Get library data, overriding anything specified as a keyword argument.
        data = {**LIBRARY.get_data(model), **kwargs}

        self.add_opamp(name, n1, n2, n3, model=LIBRARY.format_name(model), **data)
