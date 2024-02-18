"""Input component tests"""

import pytest
from zero.components import Input, Node


input_types = pytest.mark.parametrize("input_type", ("voltage", "current"))


@input_types
def test_signal_input(input_type):
    inpt = Input(input_type=input_type, nodes=["gnd", "nin"])
    assert inpt.name == "input"
    assert inpt.input_type == input_type
    assert inpt.nodes == [Node("gnd"), Node("nin")]
    assert inpt.node1 == Node("gnd")
    assert inpt.node2 == Node("nin")
    assert inpt.node_n == inpt.node1
    assert inpt.node_p == inpt.node2


@input_types
def test_noise_input(input_type):
    inpt = Input(input_type=input_type, nodes=["gnd", "nin"], is_noise=True, impedance="15.5k")
    assert inpt.name == "input"
    assert inpt.input_type == input_type
    assert inpt.impedance == 15.5e3
    assert inpt.nodes == [Node("gnd"), Node("nin")]
    assert inpt.node1 == Node("gnd")
    assert inpt.node2 == Node("nin")
    assert inpt.node_n == inpt.node1
    assert inpt.node_p == inpt.node2


@input_types
def test_name_cannot_be_set(input_type):
    with pytest.raises(TypeError):
        Input(name="abc", input_type=input_type, nodes=["gnd", "nin"])


@input_types
def test_input_impedance(input_type):
    inpt = Input(input_type=input_type, nodes=["gnd", "nin"])
    assert inpt.impedance is None
