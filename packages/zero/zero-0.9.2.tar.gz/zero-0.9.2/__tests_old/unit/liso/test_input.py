"""LISO input parser tests"""

import numpy as np
import pytest

from zero.liso import LisoInputParser, LisoParserError
from zero.components import Node, NoiseNotFoundError


@pytest.fixture
def parser():
    return LisoInputParser()


def test_resistor(parser):
    parser.parse("r r1 10k n1 n2")
    r = parser.circuit["r1"]
    assert r.name == "r1"
    assert r.resistance == pytest.approx(10e3)
    assert r.node1 == Node("n1")
    assert r.node2 == Node("n2")


def test_capacitor(parser):
    parser.parse("c c1 10n n1 n2")
    c = parser.circuit["c1"]
    assert c.name == "c1"
    assert c.capacitance == pytest.approx(10e-9)
    assert c.node1 == Node("n1")
    assert c.node2 == Node("n2")


def test_inductor(parser):
    parser.parse("l l1 10u n1 n2")
    l = parser.circuit["l1"]
    assert l.name == "l1"
    assert l.inductance == pytest.approx(10e-6)
    assert l.node1 == Node("n1")
    assert l.node2 == Node("n2")


def test_opamp(parser):
    parser.parse("op op1 OP00 n1 n2 n3")
    op = parser.circuit["op1"]
    assert op.name == "op1"
    assert op.model.lower() == "op00"
    assert op.node1 == Node("n1")
    assert op.node2 == Node("n2")
    assert op.node3 == Node("n3")


def test_invalid_model(parser):
    with pytest.raises(ValueError, match=r"op-amp model '__opinvalid__' not found in library"):
        parser.parse("op op1 __opinvalid__ n1 n2 n3")


def test_opamp_override(parser):
    parser.parse("op op1 op27 n1 n2 n3 a0=123M")
    op = parser.circuit["op1"]
    assert op.params["a0"] == pytest.approx(123e6)

    parser.parse("op op2 ad797 n4 n5 n6 a0=123M gbw=456k")
    op = parser.circuit["op2"]
    assert op.params["a0"] == pytest.approx(123e6)
    assert op.params["gbw"] == pytest.approx(456e3)

    parser.parse("op op3 lt1124 n4 n5 n6 a0=123M gbw=456k sr=1G")
    op = parser.circuit["op3"]
    assert op.params["a0"] == pytest.approx(123e6)
    assert op.params["gbw"] == pytest.approx(456e3)
    assert op.params["sr"] == pytest.approx(1e9)


def test_opamp_invalid_override(parser):
    with pytest.raises(
        LisoParserError, match=r"unknown op-amp override parameter 'a1' \(line 3\)"
    ):
        parser.parse(
            text="""
            r r1 430 n1 nm
            op op1 op27 np nm nout a1=123e6
            c c1 10u gnd n1
            """
        )


@pytest.mark.parametrize(
    "script,frequencies",
    (
        ("freq lin 0.1 100k 1000", np.linspace(1e-1, 1e5, 1001)),
        ("freq log 0.1 100k 1000", np.logspace(np.log10(1e-1), np.log10(1e5), 1001)),
        ("freq lin 1e-3 1e5 1000", np.linspace(1e-3, 1e5, 1001)),
    )
)
def test_frequencies(parser, script, frequencies):
    parser.parse(script)
    assert np.allclose(parser.frequencies, frequencies)


def test_invalid_scale(parser):
    with pytest.raises(LisoParserError, match=r"invalid frequency scale 'dec' \(line 3\)"):
        parser.parse(
            """
            r r1 430 n1 nm
            freq dec 1 1M 1234
            c c1 10u gnd n1
            """
        )


def test_cannot_redefine_frequencies(parser):
    parser.parse("freq lin 0.1 100k 1000")
    # try to set frequencies again
    with pytest.raises(LisoParserError, match=r"cannot redefine frequencies \(line 2\)"):
        parser.parse("freq lin 0.1 100k 1000")


def test_voltage_input(parser):
    parser.parse("uinput nin")
    assert parser.input_type == "voltage"
    assert parser.input_node_p == Node("nin")
    assert parser.input_node_n is None


def test_cannot_redefine_voltage_input_type(parser):
    parser.parse("uinput nin")
    # try to set input again
    with pytest.raises(LisoParserError, match=r"cannot redefine input type \(line 2\)"):
        parser.parse("uinput nin")


@pytest.mark.parametrize(
    "impedance,parsed_impedance",
    (
        ("", 50),
        ("10M", 10e6),
        ("1e3", 1e3),
    )
)
def test_voltage_input_impedance(parser, impedance, parsed_impedance):
    parser.parse(f"uinput nin {impedance}")
    assert parser.input_impedance == parsed_impedance


def test_current_input(parser):
    parser.parse("iinput nin")
    assert parser.input_type == "current"
    assert parser.output_type is None
    assert parser.input_node_p == Node("nin")
    assert parser.input_node_n is None


def test_cannot_redefine_current_input_type(parser):
    parser.parse("iinput nin")
    # try to set input again
    with pytest.raises(LisoParserError, match=r"cannot redefine input type \(line 2\)"):
        parser.parse("iinput nin")


@pytest.mark.parametrize(
    "impedance,parsed_impedance",
    (
        ("", 50),
        ("10M", 10e6),
        ("1e3", 1e3),
    )
)
def test_current_input_impedance(parser, impedance, parsed_impedance):
    parser.parse(f"iinput nin {impedance}")
    assert parser.input_impedance == parsed_impedance


def test_noise(parser):
    parser.parse("noise nout n1")
    assert parser.output_type == "noise"
    assert parser.noise_output_element == "nout"


@pytest.mark.parametrize(
    "suffix,nobj",
    (
        ("op1:u", 1),
        ("op1:u+-", 3),
        ("op1:-u+", 3)
    )
)
def test_noise_suffices(parser, suffix, nobj):
    parser.parse(
        """
        r r1 1k n1 n3
        r r2 10k n3 n4
        r r3 10k n2 gnd
        op op1 op00 n2 n3 n4
        """
    )
    parser.parse(f"noise nout {suffix}")
    assert len(parser.displayed_noise_objects) == nobj


def test_cannot_redefine_noise_node(parser):
    parser.parse("noise nout n1")
    # try to set noise node again
    with pytest.raises(LisoParserError, match=r"cannot redefine noise output element \(line 2\)"):
        parser.parse("noise nin n1")


def test_must_set_noise_output_element(parser):
    # sink element defined, but no sources
    with pytest.raises(LisoParserError, match=r"unexpected end of file \(line 1\)"):
        parser.parse("noise nout")


@pytest.mark.parametrize(
    "suffix",
    ("r2:u", "r2:+", "r2:-")
)
def test_cannot_set_scaling_for_non_opamp(parser, suffix):
    # try to set resistor voltage noise
    parser.parse(
        """
        r r1 1k n1 n2
        r r2 10k n2 n3
        op op1 op00 gnd n2 n3
        """
    )
    parser.parse(f"noise n3 {suffix}")
    with pytest.raises(
        LisoParserError, match=r"noise suffices cannot be specified on non-op-amps \(line 6\)"
    ):
        getattr(parser, "displayed_noise_objects")


def test_cannot_set_noisy_sum(parser):
    parser.parse(
        """
        r r1 1k n1 n2
        r r2 10k n2 n3
        op op1 op00 gnd n2 n3
        """
    )
    parser.parse("noisy sum")
    with pytest.raises(LisoParserError, match=r"cannot specify 'sum' as noisy source \(line 6\)"):
        getattr(parser, "summed_noise_objects")


@pytest.mark.parametrize(
    "script,error",
    (
        (
            # Component type "a" doesn't exist.
            """
            a c1 10u gnd n1
            r r1 430 n1 nm
            """,
            r"'a' \(line 2\)"
        ),
        (
            # No component name given.
            """
            c 10u gnd n1
            r r1 430 n1 nm
            """,
            r"unexpected end of line \(line 2\)"
        ),
        (
            # No component name given, extra newline.
            """
            c 10u gnd n1

            r r1 430 n1 nm
            """,
            r"unexpected end of line \(line 2\)"
        ),
        (
            # Invalid component value.
            """
            r r1 430 n1 nm
            c c1 -10u gnd n1
            """,
            r"illegal character '-' \(line 3, position 17\)"
        ),
        (
            # Invalid component value.
            """
            r r1 430 n1 nm
            c c1 10u gnd @
            """,
            r"illegal character '@' \(line 3, position 25\)"
        )
    )
)
def test_invalid_component(parser, script, error):
    with pytest.raises(LisoParserError, match=error):
        parser.parse(script)
