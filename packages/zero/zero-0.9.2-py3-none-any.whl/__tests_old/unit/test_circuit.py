"""Circuit tests"""

import re
from copy import deepcopy
import pytest
import numpy as np

from zero.components import Resistor, Capacitor, Inductor, OpAmp, Node
from zero.analysis import AcSignalAnalysis


component_params = pytest.mark.parametrize(
    "component",
    (
        Resistor(name="r1", value=10e3, node1="n1", node2="n2"),
        Capacitor(name="c1", value="10u", node1="n1", node2="n2"),
    )
)


def test_add_component(circuit):
    """Test add component to circuit"""
    resistor = Resistor(name="r1", value=10e3, node1="n1", node2="n2")
    capacitor = Capacitor(name="c1", value="10u", node1="n1", node2="n2")
    inductor = Inductor(name="l1", value="1u", node1="n1", node2="n2")

    circuit.add_component(resistor)
    assert circuit.n_components == 1
    assert circuit.n_nodes == 2
    assert set(circuit.components) == set([resistor])
    assert set(circuit.non_gnd_nodes) == set([Node("n1"), Node("n2")])

    circuit.add_component(capacitor)
    assert circuit.n_components == 2
    assert circuit.n_nodes == 2
    assert set(circuit.components) == set([resistor, capacitor])
    assert set(circuit.non_gnd_nodes) == set([Node("n1"), Node("n2")])

    circuit.add_component(inductor)
    assert circuit.n_components == 3
    assert circuit.n_nodes == 2
    assert set(circuit.components) == set([resistor, capacitor, inductor])
    assert set(circuit.non_gnd_nodes) == set([Node("n1"), Node("n2")])


@pytest.mark.parametrize(
    "component,name_before,name_after",
    (
        # Nameless.
        (Resistor(value=10e3, node1="n1", node2="n2"), None, "r1"),
        (Capacitor(value="10u", node1="n1", node2="n2"), None, "c1"),
        (Inductor(value="1u", node1="n1", node2="n2"), None, "l1"),
        (OpAmp(model="OP00", node1="n1", node2="n2", node3="n3"), None, "op1"),
        # With name already.
        (Resistor(name="r2", value=10e3, node1="n1", node2="n2"), "r2", "r2"),
        (Capacitor(name="c3", value="10u", node1="n1", node2="n2"), "c3", "c3"),
        (Inductor(name="hello", value="1u", node1="n1", node2="n2"), "hello", "hello"),
        (OpAmp(name="myop", model="OP00", node1="n1", node2="n2", node3="n3"), "myop", "myop"),
    )
)
def test_add_component_assigns_name_if_required(circuit, component, name_before, name_after):
    assert component.name == name_before
    circuit.add_component(component)
    assert component.name == name_after


@component_params
def test_remove_component(circuit, component):
    circuit.add_component(component)
    assert set(circuit.components) == set([component])
    assert circuit.n_components == 1
    circuit.remove_component(component)
    assert not circuit.components
    assert circuit.n_components == 0


@component_params
def test_remove_component_by_name(circuit, component):
    circuit.add_component(component)
    assert set(circuit.components) == set([component])
    assert circuit.n_components == 1
    circuit.remove_component(component.name)
    assert not circuit.components
    assert circuit.n_components == 0


@pytest.mark.parametrize(
    "component,error",
    (
        (
            Resistor(name="all", value=1, node1="n1", node2="n2"),
            "component name 'all' is reserved",
        ),
        (
            Capacitor(name="sum", value=1, node1="n1", node2="n2"),
            "component name 'sum' is reserved",
        ),
    )
)
def test_cannot_add_component_with_invalid_name(circuit, component, error):
    """Test components with invalid names cannot be added to circuit"""
    with pytest.raises(ValueError, match=re.escape(error)):
        circuit.add_component(component)


@pytest.mark.parametrize(
    "components,error",
    (
        # Same types; same names.
        (
            [
                Resistor(name="r1", value=1e3, node1="n1", node2="n2"),
                Resistor(name="r1", value=2e5, node1="n3", node2="n4"),
            ],
            "element with name 'r1' already in circuit"
        ),
        (
            [
                Resistor(name="r1", value=1e3, node1="n1", node2="n2"),
                OpAmp(name="r1", model="OP00", node1="n3", node2="n4", node3="n5"),
            ],
            "element with name 'r1' already in circuit"
        ),
        # Second component name is the same as one of the first component's nodes.
        (
            [
                Resistor(name="r1", value=1e3, node1="n1", node2="n2"),
                Resistor(name="n1", value=2e5, node1="n3", node2="r4"),
            ],
            "element with name 'n1' already in circuit"
        ),
        (
            [
                Resistor(name="r1", value=1e3, node1="n1", node2="n2"),
                OpAmp(name="n2", model="OP00", node1="n2", node2="n4", node3="n5"),
            ],
            "element with name 'n2' already in circuit"
        ),
        # Second component node has same name as first component.
        (
            [
                Resistor(name="r1", value=1e3, node1="n1", node2="n2"),
                Resistor(name="r2", value=2e5, node1="n3", node2="r1"),
            ],
            "node 'r1' is the same as existing circuit component"
        ),
        (
            [
                Resistor(name="r1", value=1e3, node1="n1", node2="n2"),
                OpAmp(name="op1", model="OP00", node1="r1", node2="n4", node3="n5"),
            ],
            "node 'r1' is the same as existing circuit component"
        )
    )
)
def test_cannot_add_same_identifier_names(circuit, components, error):
    with pytest.raises(ValueError, match=re.escape(error)):
        for component in components:
            circuit.add_component(component)


@pytest.mark.parametrize(
    "cmp1,cmp2",
    (
        (
            Resistor(name="r1", value="1k", node1="n1", node2="n2"),
            Resistor(name="r2", value="1k", node1="n3", node2="n4")
        ),
        (
            OpAmp(name="op1", model="OP00", node1="n1", node2="n2", node3="n3"),
            OpAmp(name="op2", model="OP00", node1="n4", node2="n5", node3="n6"),
        ),
    )
)
def test_replace(circuit, cmp1, cmp2):
    circuit.add_component(cmp1)
    assert circuit.has_component(cmp1.name)
    circuit.replace_component(cmp1, cmp2)
    # Test circuit composition.
    assert circuit.has_component(cmp2.name)
    assert not circuit.has_component(cmp1.name)
    # Nodes in cmp2 should have been copied from cmp1.
    assert cmp1.nodes == cmp2.nodes


@pytest.mark.parametrize(
    "cmp1,cmp2",
    (
        (
            Resistor(name="r1", value="1k", node1="n1", node2="n2"),
            OpAmp(name="op1", model="OP00", node1="n1", node2="n2", node3="n3"),
        ),
        (
            OpAmp(name="op2", model="OP00", node1="n4", node2="n5", node3="n6"),
            Resistor(name="r2", value="1k", node1="n3", node2="n4")
        ),
    )
)
def test_cannot_replace_passive_opamp_or_opamp_passive(circuit, cmp1, cmp2):
    """Test passive components cannot be replaced with op-amps (and vice versa)."""
    circuit.add_component(cmp1)
    assert circuit.has_component(cmp1.name)
    with pytest.raises(ValueError):
        circuit.replace_component(cmp1, cmp2)


def test_deep_copy(circuit):
    """Test deep copying of a circuit."""
    frequencies = np.logspace(0, 3, 11)

    circuit.add_resistor(name="R1", value=50, node1="n1", node2="n2")
    circuit.add_resistor(name="R2", value=50, node1="n2", node2="gnd")
    analysis1 = AcSignalAnalysis(circuit=circuit)
    sol1 = analysis1.calculate(frequencies=frequencies, input_type="voltage", node="n1")

    # Copy the circuit.
    circuit_copy = deepcopy(circuit)

    analysis2 = AcSignalAnalysis(circuit=circuit_copy)
    sol2 = analysis2.calculate(frequencies=frequencies, input_type="voltage", node="n1")

    assert sol1.equivalent_to(sol2)
