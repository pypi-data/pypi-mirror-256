"""Mock Zero data tools."""

import numpy as np
from zero.components import (
    Resistor,
    Capacitor,
    Inductor,
    OpAmp,
    Node,
    OpAmpVoltageNoise,
    OpAmpCurrentNoise
)
from zero.solution import Solution
from zero.data import Series, Response, NoiseDensity, MultiNoiseDensity


class ZeroDataGenerator:
    """Zero data generator."""
    def __init__(self, seed=2543070):
        self._last_node_num = 0
        self._last_resistor_num = 0
        self._last_capacitor_num = 0
        self._last_inductor_num = 0
        self._last_opamp_num = 0

        np.random.seed(seed=seed)

    def unique_node_name(self):
        self._last_node_num += 1
        return f"n{self._last_node_num}"

    def unique_resistor_name(self):
        self._last_resistor_num += 1
        return f"r{self._last_resistor_num}"

    def unique_capacitor_name(self):
        self._last_capacitor_num += 1
        return f"c{self._last_capacitor_num}"

    def unique_inductor_name(self):
        self._last_inductor_num += 1
        return f"l{self._last_inductor_num}"

    def unique_opamp_name(self):
        self._last_opamp_num += 1
        return f"op{self._last_opamp_num}"

    def data(self, shape, cplx=False):
        data = np.random.random(shape)
        if cplx:
            data = data + 1j * self.data(shape, False)
        return data

    def freqs(self, n=10):
        return np.sort(self.data(n))

    def series(self, freqs, data=None, cplx=False):
        if data is None:
            data = self.data(len(freqs), cplx)
        return Series(freqs, data)

    def node(self):
        return Node(self.unique_node_name())

    def opamp(self, node1=None, node2=None, node3=None, model=None):
        if node1 is None:
            node1 = self.node()
        if node2 is None:
            node2 = self.node()
        if node3 is None:
            node3 = self.node()
        if model is None:
            model = "OP00"
        return OpAmp(name=self.unique_opamp_name(), model=model, node1=node1, node2=node2,
                     node3=node3)

    def resistor(self, node1=None, node2=None, value=None):
        if node1 is None:
            node1 = self.node()
        if node2 is None:
            node2 = self.node()
        if value is None:
            value = "1k"
        return Resistor(name=self.unique_resistor_name(), node1=node1, node2=node2, value=value)

    def capacitor(self, node1=None, node2=None, value=None):
        if node1 is None:
            node1 = self.node()
        if node2 is None:
            node2 = self.node()
        if value is None:
            value = "1u"
        return Capacitor(name=self.unique_capacitor_name(), node1=node1, node2=node2, value=value)

    def inductor(self, node1=None, node2=None, value=None):
        if node1 is None:
            node1 = self.node()
        if node2 is None:
            node2 = self.node()
        if value is None:
            value = "1u"
        return Inductor(name=self.unique_inductor_name(), node1=node1, node2=node2, value=value)

    def voltage_noise(self, component=None):
        if component is None:
            component = self.resistor()
        return OpAmpVoltageNoise(component=component)

    def current_noise(self, node=None, component=None):
        if node is None:
            node = self.node()
        if component is None:
            component = self.resistor(node1=node)
        return OpAmpCurrentNoise(node=node, component=component)

    def response(self, source, sink, freqs):
        return Response(source=source, sink=sink, series=self.series(freqs, cplx=True))

    def v_v_response(self, freqs, node_source=None, node_sink=None):
        if node_source is None:
            node_source = self.node()
        if node_sink is None:
            node_sink = self.node()
        return self.response(node_source, node_sink, freqs)

    def v_i_response(self, freqs, node_source=None, component_sink=None):
        if node_source is None:
            node_source = self.node()
        if component_sink is None:
            component_sink = self.resistor()
        return self.response(node_source, component_sink, freqs)

    def i_i_response(self, freqs, component_source=None, component_sink=None):
        if component_source is None:
            component_source = self.resistor()
        if component_sink is None:
            component_sink = self.resistor()
        return self.response(component_source, component_sink, freqs)

    def i_v_response(self, freqs, component_source=None, node_sink=None):
        if component_source is None:
            component_source = self.resistor()
        if node_sink is None:
            node_sink = self.node()
        return self.response(component_source, node_sink, freqs)

    def noise_density(self, freqs, source, sink):
        return NoiseDensity(source=source, sink=sink, series=self.series(freqs))

    def vnoise_at_node(self, freqs, source=None, sink=None):
        if source is None:
            source = self.voltage_noise()
        if sink is None:
            sink = self.node()
        return self.noise_density(freqs, source, sink)

    def vnoise_at_comp(self, freqs, source=None, sink=None):
        if source is None:
            source = self.voltage_noise()
        if sink is None:
            sink = self.resistor()
        return self.noise_density(freqs, source, sink)

    def inoise_at_node(self, freqs, source=None, sink=None):
        if source is None:
            source = self.current_noise()
        if sink is None:
            sink = self.node()
        return self.noise_density(freqs, source, sink)

    def inoise_at_comp(self, freqs, source=None, sink=None):
        if source is None:
            source = self.current_noise()
        if sink is None:
            sink = self.resistor()
        return self.noise_density(freqs, source, sink)

    def multi_noise_density(self, sink, constituents, label=None):
        return MultiNoiseDensity(sink=sink, constituents=constituents, label=label)

    def solution(self, freq):
        return Solution(freq)
