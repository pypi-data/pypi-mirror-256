"""Electronic components: circuits, resistors, capacitors, inductors."""

import abc
from collections import defaultdict
from collections.abc import MutableMapping
from itertools import chain
from enum import auto, Enum
import re
import weakref
from copy import copy

import numpy as np

from .format import Quantity
from .misc import db_to_mag
from .noise import OpAmpVoltageNoise, OpAmpCurrentNoise, ResistorJohnsonNoise
from .tools import validate_name


class BaseComponent(metaclass=abc.ABCMeta):
    """Interface defining a component."""

    # Flag designating that the component generates a voltage.
    GENERATES_VOLTAGE = False

    def __init__(self, name, nodes):
        name = str(name)
        validate_name(name)

        self.name = name
        self.nodes = tuple(nodes)
        for index, node in enumerate(nodes, start=1):
            setattr(self, f"n{index}", node)

    def fill_dc(self, mna, i_index):
        return

    def fill_sources(self, sources, i_index):
        return

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name} @ {hex(id(self))}>"


class VSource(BaseComponent):
    """An ideal voltage source."""

    GENERATES_VOLTAGE = True

    def __init__(self, name, n1, n2, dc_value, ac_value=0):
        super().__init__(name, [n1, n2])
        self.dc_value = dc_value
        self.ac_value = ac_value

    def voltage(self):
        """Evaluate the voltage applied by the source."""
        return self.dc_value

    def fill_dc(self, mna, i_index):
        # KCL.
        mna[self.n1, i_index] = 1.0
        mna[self.n2, i_index] = -1.0
        # KVL.
        mna[i_index, self.n1] = 1.0
        mna[i_index, self.n2] = -1.0

    def fill_sources(self, sources, i_index):
        sources[i_index, 0] = -1.0 * self.voltage()


class ISource(BaseComponent):
    """An ideal current source."""
    def __init__(self, name, n1, n2, dc_value, ac_value=0):
        super().__init__(name, [n1, n2])
        self.dc_value = dc_value
        self.ac_value = ac_value

    def current(self):
        """Evaluate the current forced by the source."""
        return self.dc_value

    def fill_sources(self, sources, _):
        current = self.current()
        sources[self.n1, 0] += current
        sources[self.n2, 0] -= current


class PassiveComponent(BaseComponent, metaclass=abc.ABCMeta):
    """A passive component.

    A passive component is one that consumes or temporarily stores energy, but does not produce or
    amplify it.

    Parameters
    ----------
    name : :class:`str`, optional
        The component name. Must be unique. Once the name is set, it cannot be changed.
    value : any
        The component value.
    """
    def __init__(self, name, value, n1, n2):
        super().__init__(name, [n1, n2])
        self.value = Quantity(value)


class Resistor(PassiveComponent):
    """An ideal resistor."""

    def gain(self):
        return 1 / self.value

    def fill_dc(self, mna, _):
        gain = self.gain()
        mna[self.n1, self.n1] += gain
        mna[self.n1, self.n2] -= gain
        mna[self.n2, self.n1] -= gain
        mna[self.n2, self.n2] += gain


class Capacitor(PassiveComponent):
    """An ideal capacitor."""


class Inductor(PassiveComponent):
    """An ideal inductor."""

    GENERATES_VOLTAGE = True

    def fill_dc(self, mna, i_index):
        # KCL.
        mna[self.n1, i_index] = 1.0
        mna[self.n2, i_index] = -1.0
        # KVL.
        mna[i_index, self.n1] = 1.0
        mna[i_index, self.n2] = -1.0


class OpAmp(BaseComponent):
    """An operational amplifier.

    An op-amp produces :class:`voltage noise <VoltageNoise>` across its input
    and output :class:`nodes <Node>`, and :class:`current noise <CurrentNoise>`
    is present at its input :class:`nodes <Node>`.

    The default parameters represent a typical op-amp.

    Parameters
    ----------
    a0 : :class:`float`, optional
        Open loop gain.
    gbw : :class:`float`, optional
        Gain-bandwidth product.
    delay : :class:`float`, optional
        Delay.
    zeros : sequence, optional
        Zeros.
    poles : sequence, optional
        Poles.
    vnoise : :class:`float`, optional
        Flat voltage noise.
    vcorner : :class:`float`, optional
        Voltage noise corner frequency.
    inoise : :class:`float`, optional
        Flat current noise.
    icorner : :class:`float`, optional
        Current noise corner frequency.
    vmax : :class:`float`, optional
        Maximum input voltage.
    imax : :class:`float`, optional
        Maximum output current.
    sr : :class:`float`, optional
        Slew rate.
    """
    def __init__(
        self,
        name,
        a0=1.5e6,
        gbw=8e6,
        delay=0,
        zeros=np.array([]),
        poles=np.array([]),
        vnoise=3.2e-9,
        vcorner=2.7,
        inoise=0.4e-12,
        icorner=140
    ):
        super().__init__(name)

        self._register_internal_node("ninp", InternalNodeType.VOLTAGE)
        self._register_internal_node("ninm", InternalNodeType.VOLTAGE)
        self._register_internal_node("nout", InternalNodeType.VOLTAGE)
        self._register_internal_node("i", InternalNodeType.CURRENT)

        self._register_internal_node_coupling("ninp->nout", self.ninp, self.nout)
        self._register_internal_node_coupling("ninm->nout", self.ninm, self.nout)
        self._register_internal_node_coupling("i->nout", self.i, self.nout)

        self._register_noise(OpAmpVoltageNoise)
        self._register_noise(OpAmpCurrentNoise, node="ninp")
        self._register_noise(OpAmpCurrentNoise, node="ninm")

    @property
    def a0(self):
        """Gain"""
        return self.params["a0"]

    @a0.setter
    def a0(self, a0):
        try:
            a0 = a0.strip()
            if a0[-2:].casefold() == "db":
                # Convert decibels to absolute magnitude.
                a0 = db_to_mag(float(a0[:-2].strip()))
        except AttributeError:
            # It's probably a number.
            pass

        self.params["a0"] = Quantity(a0, "V/V")

    @property
    def gbw(self):
        """Gain-bandwidth product"""
        return self.params["gbw"]

    @gbw.setter
    def gbw(self, gbw):
        self.params["gbw"] = Quantity(gbw, "Hz")

    @property
    def delay(self):
        """Delay"""
        return self.params["delay"]

    @delay.setter
    def delay(self, delay):
        self.params["delay"] = Quantity(delay, "s")

    @property
    def zeros(self):
        """Additional zeros"""
        return self.params["zeros"]

    @zeros.setter
    def zeros(self, zeros):
        self.params["zeros"] = np.array(zeros)

    @property
    def zeros_mag_q(self):
        """Additional zeros, in tuples containing magnitude and Q-factor"""
        return self._mag_q_pairs(self.zeros)

    @property
    def poles(self):
        """Additional poles"""
        return self.params["poles"]

    @poles.setter
    def poles(self, poles):
        self.params["poles"] = np.array(poles)

    @property
    def poles_mag_q(self):
        """Additional poles, in tuples containing magnitude and Q-factor"""
        return self._mag_q_pairs(self.poles)

    @property
    def vnoise(self):
        """Voltage noise"""
        return self.params["vnoise"]

    @vnoise.setter
    def vnoise(self, vnoise):
        self.params["vnoise"] = Quantity(vnoise, "V/sqrt(Hz)")

    @property
    def vcorner(self):
        """Voltage noise corner frequency"""
        return self.params["vcorner"]

    @vcorner.setter
    def vcorner(self, vcorner):
        self.params["vcorner"] = Quantity(vcorner, "Hz")

    @property
    def inoise(self):
        """Current noise"""
        return self.params["inoise"]

    @inoise.setter
    def inoise(self, inoise):
        self.params["inoise"] = Quantity(inoise, "A/sqrt(Hz)")

    @property
    def icorner(self):
        """Current noise corner frequency"""
        return self.params["icorner"]

    @icorner.setter
    def icorner(self, icorner):
        self.params["icorner"] = Quantity(icorner, "Hz")


class CouplingFactorDict(MutableMapping):
    """Collection to get and set coupling factors between inductors.

    This is essentially a :class:`dict` that allows only inductors as keys and a certain range of
    values.
    """
    def __init__(self, *args, **kwargs):
        # create dict to store things
        self._couplings = dict()

        # initialise data
        self.update(dict(*args, **kwargs))

    def __getitem__(self, inductor):
        """Get coupling factor for specified inductor

        If there is no coupling factor defined between the inductors, it is assumed to be zero.

        Parameters
        ----------
        inductor : :class:`.Inductor`
            The inductor to get the coupling for.

        Returns
        -------
        :class:`float`
            The coupling factor.

        Raises
        ------
        :class:`TypeError`
            If the specified component is not an inductor.
        """
        if not isinstance(inductor, Inductor):
            raise TypeError(f"{repr(inductor)} must be an inductor")

        return self._couplings.get(inductor, 0)

    def __setitem__(self, inductor, coupling_factor):
        """Set coupling factor for specified inductor

        Parameters
        ----------
        inductor : :class:`.Inductor`
            The inductor to couple to the inductor contained within this.
        coupling_factor : any
            The coupling factor to use.

        Raises
        ------
        :class:`TypeError`
            If the specified component is not an inductor.
        :class:`ValueError`
            If the specified coupling factor is outside the range [0, 1].
        """
        if not isinstance(inductor, Inductor):
            raise TypeError(f"{repr(inductor)} must be an inductor")

        coupling_factor = Quantity(coupling_factor)
        if 0 > coupling_factor > 1:
            raise ValueError("Coupling factor must be between 0 and 1")

        self._couplings[inductor] = coupling_factor

    def __delitem__(self, key):
        del self._couplings[key]

    def __iter__(self):
        return iter(self._couplings)

    def __len__(self):
        return len(self._couplings)

    def __contains__(self, key):
        return key in self._couplings
