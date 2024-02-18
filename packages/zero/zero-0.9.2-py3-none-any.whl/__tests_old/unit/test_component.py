"""Component tests"""

import pytest
from zero.components import Component as ComponentBase, Resistor, Capacitor, Inductor, Node


class MockComponent(ComponentBase):
    """Child class of abstract ComponentBase, used to test :class:`components <.Component>` \
    directly"""
    def equation(self):
        """Mock component equation (not needed for tests)"""
        raise NotImplementedError


@pytest.mark.parametrize(
    "name,expected",
    (
        ("", ""),
        ("component_name", "component_name"),
        ("null", "null"),
        (None, None),
    )
)
def test_name(name, expected):
    assert MockComponent(name=name).name == expected


@pytest.mark.parametrize(
    "nodes,expected",
    (
        ([], []),
        ([Node("n1"), Node("n2")], [Node("n1"), Node("n2")]),
        (None, []),
    )
)
def test_nodes(nodes, expected):
    assert MockComponent(nodes=nodes).nodes == expected


@pytest.mark.parametrize(
    "component",
    (
        Resistor(value=1, node1="n1", node2="n2"),
        Capacitor(value=1, node1="n1", node2="n2"),
        Inductor(value=1, node1="n1", node2="n2"),
    )
)
@pytest.mark.parametrize(
    "value,expected",
    (
        (101e3, 101e3),
        ("101k", 101e3),
        ("3.141p", 3.141e-12),
    )
)
def test_passive_set_value(component, value, expected):
    component.value = value
    assert float(component.value) == expected


@pytest.mark.parametrize("coupling", (0, 0.5, 1))
def test_inductor_coupling_factor(coupling):
    """Test set invalid coupling factor"""
    l1 = Inductor(value="10u", node1="n1", node2="n2")
    l2 = Inductor(value="40u", node1="n3", node2="n4")

    l1.coupling_factors[l2] = coupling
    l2.coupling_factors[l1] = coupling

    assert set(l1.coupled_inductors) == set([l2])
    assert set(l2.coupled_inductors) == set([l1])


@pytest.mark.parametrize("coupling", (-0.5, 1.1))
def test_inductor_invalid_coupling_factor(coupling):
    l1 = Inductor(value="10u", node1="n1", node2="n2")

    with pytest.raises(ValueError):
        l1.coupling_factors[l1] = coupling


@pytest.mark.parametrize(
    "target",
    (
        Resistor(value="10k", node1="n3", node2="n4"),
        Capacitor(value="10p", node1="n3", node2="n4"),
    )
)
def test_inductor_invalid_coupling_target(target):
    l1 = Inductor(value="10u", node1="n1", node2="n2")

    with pytest.raises(TypeError):
        l1.coupling_factors[target] = 1


@pytest.mark.parametrize(
    "l1,l2,c12,c21,k12,k21",
    (
        (0, 0, 0.5, 0.5, 0, 0),
        ("10u", "40u", 0.95, 0.95, 0.000019, 0.000019),
        ("10u", "40u", 0.5, 0.5, 0.00001, 0.00001),
        ("10u", "40u", 0, 0, 0, 0),
    )
)
def test_mutual_inductance(l1, l2, c12, c21, k12, k21):
    """Test set coupling factor between two inductors"""
    l1 = Inductor(value=l1, node1="n1", node2="n2")
    l2 = Inductor(value=l2, node1="n3", node2="n4")
    l1.coupling_factors[l2] = c12
    l2.coupling_factors[l1] = c21
    assert l1.inductance_from(l2) == pytest.approx(k12)
    assert l2.inductance_from(l1) == pytest.approx(k21)
