"""Data tests"""

import pytest
import numpy as np
from zero.data import Series, MultiNoiseDensity
from zero.misc import mag_to_db


@pytest.fixture
def freq(datagen):
    return datagen.freqs(10)


@pytest.fixture
def data_cplx(datagen, freq):
    return datagen.data((len(freq),), cplx=True)


@pytest.fixture
def data_re(data_cplx):
    return np.real(data_cplx)


@pytest.fixture
def data_im(data_cplx):
    return np.imag(data_cplx)


@pytest.fixture
def data_mag_abs(data_cplx):
    return np.abs(data_cplx)


@pytest.fixture
def data_mag_db(data_mag_abs):
    return mag_to_db(data_mag_abs)


@pytest.fixture
def data_phase_rad(data_cplx):
    return np.angle(data_cplx)


@pytest.fixture
def data_phase_deg(data_phase_rad):
    return np.degrees(data_phase_rad)


def test_from_mag_phase_default(freq, data_mag_abs, data_phase_deg):
    lhs = Series.from_mag_phase(freq, data_mag_abs, data_phase_deg)
    rhs = Series.from_mag_phase(
        freq, data_mag_abs, data_phase_deg, mag_scale="abs", phase_scale="deg"
    )
    assert lhs == rhs


def test_from_mag_phase_abs_deg(freq, data_cplx, data_mag_abs, data_phase_deg):
    lhs = Series(freq, data_cplx)
    rhs = Series.from_mag_phase(
        freq, data_mag_abs, data_phase_deg, mag_scale="abs", phase_scale="deg"
    )
    assert lhs == rhs


def test_from_mag_phase_abs_rad(freq, data_cplx, data_mag_abs, data_phase_rad):
    lhs = Series(freq, data_cplx)
    rhs = Series.from_mag_phase(
        freq, data_mag_abs, data_phase_rad, mag_scale="abs", phase_scale="rad"
    )
    assert lhs == rhs


def test_from_mag_phase_db_deg(freq, data_cplx, data_mag_db, data_phase_rad):
    lhs = Series(freq, data_cplx)
    rhs = Series.from_mag_phase(
        freq, data_mag_db, data_phase_rad, mag_scale="db", phase_scale="rad"
    )
    assert lhs == rhs


def test_from_mag_phase_db_rad(freq, data_cplx, data_mag_db, data_phase_deg):
    lhs = Series(freq, data_cplx)
    rhs = Series.from_mag_phase(
        freq, data_mag_db, data_phase_deg, mag_scale="db", phase_scale="deg"
    )
    assert lhs == rhs


@pytest.mark.parametrize(
    "mag_scale,phase_scale",
    (
        ("ab", "rad"),
        ("abs", "ra"),
        ("db", "minute"),
    )
)
def test_from_mag_phase_invalid_scale(freq, data_mag_db, data_phase_rad, mag_scale, phase_scale):
    with pytest.raises(ValueError):
        Series.from_mag_phase(
            freq, data_mag_db, data_phase_rad, mag_scale=mag_scale, phase_scale=phase_scale
        )


def test_from_re_im(freq, data_cplx, data_re, data_im):
    lhs = Series(freq, data_cplx)
    rhs = Series.from_re_im(freq, re=data_re, im=data_im)
    assert lhs == rhs


def test_from_re_im_invalid_parts(freq):
    # Real part cannot have imaginary element.
    with pytest.raises(ValueError):
        Series.from_re_im(freq, np.array([1, 2, 3+1j]), np.array([1, 2, 3]))

    # Imaginary part cannot have imaginary element.
    with pytest.raises(ValueError):
        Series.from_re_im(freq, np.array([1, 2, 3]), np.array([1, 2, 3+1j]))


@pytest.mark.parametrize(
    "x,y",
    (
        (np.array([1, 2, 3]), np.array([1, 2, 3, 4])),
        (np.array([[1, 2, 3], [4, 5, 6]]), np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])),
    )
)
def test_invalid_shape(x, y):
    with pytest.raises(ValueError):
        Series(x=x, y=y)


def test_addition(freq, data_cplx):
    series1 = Series(freq, data_cplx)
    series2 = Series(freq, data_cplx)
    series3 = Series(freq, data_cplx)
    combined = series1 + series2 + series3
    assert np.allclose(combined.x, series1.x)
    assert np.allclose(combined.x, series2.x)
    assert np.allclose(combined.x, series3.x)
    assert np.allclose(combined.y, data_cplx * 3)


def test_addition_scalar(freq, data_cplx):
    series = Series(freq, data_cplx)
    scaled = series + 5
    assert np.allclose(scaled.x, series.x)
    assert np.allclose(scaled.y, data_cplx + 5)


def test_subtract(freq, data_cplx):
    series1 = Series(freq, data_cplx)
    series2 = Series(freq, data_cplx)
    series3 = Series(freq, data_cplx)
    combined = series1 - series2 - series3
    assert np.allclose(combined.x, series1.x)
    assert np.allclose(combined.x, series2.x)
    assert np.allclose(combined.x, series3.x)
    assert np.allclose(combined.y, data_cplx * -1)


def test_subtract_scalar(freq, data_cplx):
    series = Series(freq, data_cplx)
    scaled = series - 5
    assert np.allclose(scaled.x, series.x)
    assert np.allclose(scaled.y, data_cplx - 5)


def test_multiply(freq, data_cplx):
    series1 = Series(freq, data_cplx)
    series2 = Series(freq, data_cplx)
    series3 = Series(freq, data_cplx)
    combined = series1 * series2 * series3
    assert np.allclose(combined.x, series1.x)
    assert np.allclose(combined.x, series2.x)
    assert np.allclose(combined.x, series3.x)
    assert np.allclose(combined.y, data_cplx ** 3)


def test_multiply_self(freq, data_cplx):
    series = Series(freq, data_cplx)
    combined = series * series * series
    # Multiplication should return a new object, so there shouldn't be issues with data
    # changing later.
    series.y = np.zeros_like(series.y)
    assert np.allclose(combined.x, series.x)
    assert np.allclose(combined.y, data_cplx ** 3)


def test_multiply_scalar(freq, data_cplx):
    series = Series(freq, data_cplx)
    # Right multiplication.
    scaled = series * 5
    assert np.allclose(scaled.x, series.x)
    assert np.allclose(scaled.y, data_cplx * 5)
    # Left multiplication.
    scaled = 5 * series
    assert np.allclose(scaled.x, series.x)
    assert np.allclose(scaled.y, data_cplx * 5)


def test_divide(freq, data_cplx):
    series1 = Series(freq, data_cplx)
    series2 = Series(freq, data_cplx)
    combined = series1 / series2
    assert np.allclose(combined.x, series1.x)
    assert np.allclose(combined.y, np.ones_like(data_cplx))


def test_divide_self(freq, data_cplx):
    series = Series(freq, data_cplx)
    combined = series / series
    # Division should return a new object, so there shouldn't be issues with data changing
    # later.
    series.y = np.zeros_like(series.y)
    assert np.allclose(combined.x, series.x)
    assert np.allclose(combined.y, np.ones_like(data_cplx))


def test_divide_scalar(freq, data_cplx):
    series = Series(freq, data_cplx)
    # Right division.
    scaled = series / 5
    assert np.allclose(scaled.x, series.x)
    assert np.allclose(scaled.y, data_cplx / 5)
    # Left (reflexive) division.
    scaled = 5 / series
    assert np.allclose(scaled.x, series.x)
    assert np.allclose(scaled.y, 5 / data_cplx)


def test_exponentiate(freq, data_cplx):
    series1 = Series(freq, data_cplx)
    series2 = Series(freq, data_cplx)
    series3 = Series(freq, data_cplx)
    combined = series1 ** series2 ** series3
    assert np.allclose(combined.x, series1.x)
    assert np.allclose(combined.x, series2.x)
    assert np.allclose(combined.x, series3.x)
    assert np.allclose(combined.y, data_cplx ** data_cplx ** data_cplx)


def test_exponentiate_scalar(freq, data_cplx):
    series = Series(freq, data_cplx)
    scaled = series ** 5
    assert np.allclose(scaled.x, series.x)
    assert np.allclose(scaled.y, data_cplx ** 5)


def test_negate(freq, data_cplx):
    series = Series(freq, data_cplx)
    negated = -series
    # Negation should return a new object, so there shouldn't be issues with data changing
    # later.
    series.y = np.zeros_like(series.y)
    assert np.allclose(negated.x, series.x)
    assert np.allclose(negated.y, -data_cplx)


def test_inverse(freq, data_cplx):
    series = Series(freq, data_cplx)
    # Standard inverse.
    inverted = series.inverse()
    assert np.allclose(inverted.x, series.x)
    assert np.allclose(inverted.y, 1 / data_cplx)
    # Alternate inverse.
    inverted = 1 / series
    assert np.allclose(inverted.x, series.x)
    assert np.allclose(inverted.y, 1 / data_cplx)


def test_inverse_self(freq, data_cplx):
    series = Series(freq, data_cplx)
    inverted = series.inverse()
    # Division should return a new object, so there shouldn't be issues with data changing
    # later.
    series.y = np.zeros_like(series.y)
    assert np.allclose(inverted.x, series.x)
    assert np.allclose(inverted.y, 1 / data_cplx)


def test_constituent_noise_sum_equal_total_noise_sum(datagen):
    f = datagen.freqs()
    sink = datagen.resistor()
    noise1 = datagen.vnoise_at_comp(f, sink=sink)
    noise2 = datagen.vnoise_at_comp(f, sink=sink)  # Share sink.
    constituents = [noise1, noise2]
    sum_data = np.sqrt(sum([noise.spectral_density ** 2 for noise in constituents]))
    sum_series = datagen.series(f, sum_data)
    noisesum1 = MultiNoiseDensity(sink=sink, constituents=constituents)
    noisesum2 = MultiNoiseDensity(
        sources=[noise1.source, noise2.source], sink=sink, series=sum_series
    )
    assert noisesum1.equivalent(noisesum2)
